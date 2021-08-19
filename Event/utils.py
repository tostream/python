from multiprocessing import Process
from queue import Empty
from kombu import Connection, Queue, Exchange
from kombu.simple import SimpleQueue
from kombu.message import Message
from kombu.transport.pyamqp import Channel
from amqp.exceptions import ConsumerCancelled, RecoverableConnectionError
from abc import ABC, abstractmethod
from typing import Type, Dict, List, Optional, Tuple, Any
from jsonschema import validate
from eda_agent.log import initialize_logger
from datetime import datetime, timedelta
from sidetrade_py_api.web_api import WebApi
from sidetrade_py_api.utils import json_load_param
import functools

import socket
import argparse
import json
import os
import traceback

CONF_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "webapi": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "user": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["url", "user", "password"],
        },
        "rabbit": {
            "type": "object",
            "properties": {
                "hostname": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["hostname", "username", "password"],
        },
    },
}


ERROR_QUEUE_NAME = "ERROR_QUEUE"

QUEUE_ARGUMENTS = {"x-queue-type": "quorum"}


class Agent(ABC):
    """Perform some work on a RabbitMQ message that it receives.

    :param conf: Dictionary of configuration parameters. Try to limit a to WebApi connection string.
    :type conf: dict
    :param process_id: A process id for logging purposes
    :type process_id: int
    """

    def __init__(self, conf: dict, process_id: int):
        self.conf = conf
        self.connection: Optional[Connection] = None
        self.logger = initialize_logger("agent-%d" % process_id)

    @staticmethod
    def declare_subscribe(channel: Channel, exchange: str, queue: str) -> bool:
        """Declare a queue subscribing to the REPORTING_STAGE exchange (event)

        :param channel: An instance of ``Channel``
        :type channel: Channel
        :param exchange: The name of the RabbitMQ exchange to bind to
        :type exchange: str
        :param queue: The name of the RabbitMQ channel to bind to
        :type queue: str
        :return: True if successful
        :rtype: bool
        """
        channel.exchange_declare(
            exchange=exchange, type="fanout", durable=True, auto_delete=False
        )

        incoming_queue = Queue(
            name=queue, queue_arguments=QUEUE_ARGUMENTS, channel=channel, durable=True
        )
        incoming_queue.declare()

        channel.queue_bind(exchange=exchange, queue=queue)
        return True

    @staticmethod
    def auto_ack():
        """Whether the current agent acks incoming messages itself. We should
        avoid a situation were the message is acked twice (once in the agent and
        once in the ``ConnectionManager``), since the AMQP norm advises against it.
        False by default.

        :return: False
        :rtype: bool
        """
        return False

    @staticmethod
    def forward_errors() -> bool:
        """Whether agent errors should trigger an error forwarding to the ERROR_QUEUE, True by default.

        :return: True
        :rtype: bool
        """
        return True

    def declare(self, channel: Channel) -> bool:
        """This method is run before the agent receives messages. It can be used
        to make sure the required RabbitMQ component are correctly declared.
        False by default.

        The incoming queue is always automatically declared in the
        ``ConnectionManager``.

        :param channel: An instance of ``Channel``
        :type channel: Channel
        :return: Returns False
        :rtype: bool
        """
        return False

    @abstractmethod
    def parse_message(
        self, headers: dict, properties: dict, message: dict, raw_message: Message
    ) -> None:
        """To be created in the child class of each agent. This method should
        execute the top-level execution flow of the agent.

        :param headers: Message headers. These can be used to
            assist in message routing. See `Headers Exchange
            <https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-headers>`_
        :type headers: dict
        :param properties: Additional properties
        :type properties: dict
        :param message: The message body
        :type message: dict
        :param raw_message: an instance of ``Message``
        :type raw_message: Message
        :raises NotImplementedError: Abstract method
        """
        raise NotImplementedError(
            "Calling extract method while this has not been overridden"
        )

    def _rabbit_retry(
        f: callable, timeout: int = None
    ) -> callable:
        """A decorator to execute a method and reconnect and retry if the
        RabbitMQ connection has died

        :param f: A method of ``Agent``
        :type f: callable
        :param timeout: The number of times to attempt a reconnect, defaults to
            None (inf)
        :type timeout: int, optional
        """

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            elapsed = 0
            while True:
                try:
                    f(self, *args, **kwargs)
                    break
                except:
                    self.logger.error("".join(traceback.format_exc()))
                    self.connection = self.connection.clone()
                    self.connection.heartbeat_check()
                    elapsed += 1
                    if timeout and elapsed >= timeout:
                        raise

        return wrapper

    @_rabbit_retry
    def ack_message(self, message: Message, queue_name: str) -> None:
        """Acknowledges a message. Messages are acknowledged after the agent
        work is complete, to ensure atomicity. See `Consumer Acknowledgments
        <https://www.rabbitmq.com/confirms.html>`_

        :param message: an instance of ``Message``
        :type message: Message
        :param queue_name: The name of the message queue
        :type queue_name: str
        """
        message.ack()
        self.logger.info("Message acknowledged for %s" % queue_name)

    @_rabbit_retry
    def push_message(self, queue_name: str, message: dict) -> None:
        """Push a message in a queue. Connection management is done in the
        wrapping ``ConnectionManager`` object.

        :param queue_name: The name of the message queue
        :type queue_name: str
        :param message: A python dictionary of the message
        :type message: dict
        """

        with self.connection.Producer(routing_key=queue_name) as producer:
            producer.publish(
                json.dumps(message).encode(),
                declare=[Queue(queue_name, queue_arguments=QUEUE_ARGUMENTS)],
                confirm_publish=True,
            )

        # Send ack
        self.logger.debug("Sent message to %s" % queue_name)

    def push_event(self, exchange_name: str, message: dict):
        """Push a message to an exchange. Connection management is done in the
        wrapping ``ConnectionManager`` object.

        :param exchange_name: The name of the exchange
        :type exchange_name: str
        :param message: A python dictionary of the message
        :type message: dict
        """
        with self.connection.Producer(
            exchange=Exchange(exchange_name, "fanout")
        ) as producer:
            producer.publish(json.dumps(message).encode())


class ConnectionManager(Process):
    """Perform all the error catching when receiving messages from RabbitMQ.
    Takes as argument an ``Agent`` object that will do the actual work.

    :param queue_name: The name of the queue
    :type queue_name: str
    :param agent_class: An ``Agent`` object (not an instance)
    :type agent_class: Type[Agent]
    :param conf: Additional agent configuration
    :type conf: dict
    :param process_id: A process id for logging purposes, defaults to 1
    :type process_id: int, optional
    :param prefetch_count: The number of advance messages to cache locally while
        the current message is being worked on, defaults to 1
    :type prefetch_count: int, optional
    """

    def __init__(
        self,
        queue_name: str,
        agent_class: Type[Agent],
        conf: dict,
        process_id: int = 1,
        prefetch_count: int = 1,
    ):
        Process.__init__(self)
        self.queue_name = queue_name
        self.conf = conf

        self.agent_class = agent_class
        self.agent: Optional[Agent] = None

        self.prefetch_count = prefetch_count
        self.process_id = process_id
        self.stopped = False

        self.logger = initialize_logger("manager-%d" % self.process_id)

        self.hostname, self.username, self.password = self.get_connection_config(conf)

    def get_connection_config(self, conf: dict) -> Tuple[str]:
        """Fetch the RabbitMQ connection details from Metabase using
            ``sidetrade_py_api.web_api.WebApi``

        :param conf: A dictionary containing the WebApi url and credentials, in
            the following format:
        :type conf: dict
        
        ::
            
            {
                "webapi": {
                    "url": "http://domain:port/api",
                    "user": "username",
                    "password": "password"
                }
            }

        :return: hostname, user, password
        :rtype: Tuple[str]
        """
        rabbit_conf = {}

        if conf.get("webapi"):
            api_conf = conf["webapi"]
            api = WebApi(api_conf["url"], api_conf["user"], api_conf["password"])
            rabbit_conf_str = api.get_global_meta_parameter("RabbitMQ", "v2")
            rabbit_conf = json_load_param(rabbit_conf_str)
        elif conf.get("rabbit"):
            rabbit_conf = conf["rabbit"]
            self.logger.warning(
                """Passing RabbitMQ connection details via Ansible
                is marked for deprecation, use the webapi instead""",
            )
        try:
            return (
                rabbit_conf["hostname"],
                rabbit_conf["username"],
                rabbit_conf["password"],
            )
        except KeyError:
            raise Exception('Credentials not found, check Metabase or your Ansible configuration')

    def declare(self, agent: Agent) -> None:
        """Perform declaration on the RabbitMQ schema (queues, exchanges,
            bindings, ...).

        :param agent: An ``Agent`` instance
        :type agent: Agent
        """
        with Connection(
            "amqp://" + self.username + ":" + self.password + "@" + self.hostname + "/"
        ) as conn:
            with conn.channel() as channel:
                # Declare the error queue

                error_queue = Queue(
                    name=ERROR_QUEUE_NAME,
                    queue_arguments=QUEUE_ARGUMENTS,
                    channel=channel,
                )
                error_queue.declare()

                # If there isn't a custom queue declare, default it
                if agent.declare(channel) is False:
                    # Declare the incoming queue
                    incoming_queue = Queue(
                        name=self.queue_name,
                        queue_arguments=QUEUE_ARGUMENTS,
                        channel=channel,
                    )
                    incoming_queue.declare()

    def run(self) -> None:
        """Creates the instance of ``Agent``, the RabbitMQ channel
        and queue, starts an infinite loop that receives a message, and
        calls ``ConnectionManager.process_message()``"""

        # Create agent
        self.agent = self.agent_class(self.conf, self.process_id)
        # Declare queues
        self.declare(self.agent)

        while True:
            try:
                with Connection(
                    "amqp://"
                    + self.username
                    + ":"
                    + self.password
                    + "@"
                    + self.hostname
                    + "/"
                ) as conn:
                    with conn.channel() as channel:
                        self.agent.connection = conn
                        channel.basic_qos(0, self.prefetch_count, False)

                        with conn.SimpleQueue(
                            self.queue_name,
                            channel=channel,
                            no_ack=False,
                            queue_args=QUEUE_ARGUMENTS,
                        ) as queue:
                            self.process_message(queue, conn)

                            if self.stopped:
                                return

                            self.logger.error(
                                "Reconnecting... [PID %s]" % (os.getpid())
                            )

            except (ConsumerCancelled, ConnectionResetError, BrokenPipeError, OSError):
                self.logger.error("".join(traceback.format_exc()))
                continue
            except:
                self.logger.error("When disconnecting, got exception:")
                self.logger.error("".join(traceback.format_exc()))
                raise

    def process_message(self, queue: SimpleQueue, conn: Connection) -> None:
        """Do the actual work required for the message by calling the ``Agent``. Acknowledge the message when completed
        Handle the following types of exceptions:

        - RabbitMQ Connection error
        - Message empty
        - Agent not instantiated
        
        Handles exceptions in the following manner:

        - Attempt message requeue
        - Forward the traceback to the ERROR_QUEUE

        :param queue: An instance of ``SimpleQueue`` created by ``ConnectionManager.run()``
        :type queue: SimpleQueue
        :param conn: The ``Connection`` created by ``ConnectionManager.run()``
        :type conn: Connection
        """

        last_message_time = datetime.now()
        # While listener is not stopped and less than 800 seconds have passed since the
        # last message was received.
        # See https://gitlab.com/sidetrade/python/eda-agent/-/issues/13 for more details
        while not self.stopped and (
            datetime.now() - last_message_time < timedelta(seconds=800)
        ):
            message = None
            try:
                # Wait for the next message (1 sec, to stop properly)
                message = queue.get(timeout=1)
            except (ConsumerCancelled, ConnectionResetError, BrokenPipeError, OSError):
                # Reconnect
                return
            except Empty:
                continue
            except:
                self.logger.error("".join(traceback.format_exc()))
                if message is not None:
                    # In case of a keyboard interrupt, message can be None
                    message.requeue()
                raise

            last_message_time = datetime.now()
            try:
                assert self.agent is not None
                # Parses message
                body = json.loads(message.body.decode())
                # Log message contents for replication purposes
                self.logger.info("Message Body Received: %s", body)
                self.agent.parse_message(
                    message.headers, message.properties, body, message
                )

                if not self.agent.auto_ack():
                    # Send ack
                    self.agent.ack_message(message, self.queue_name)
            # Network/Rabbit issue
            except (ConsumerCancelled, ConnectionResetError, BrokenPipeError, OSError):
                # Reconnect
                return
            # Processing issue
            except:
                # Send unack message
                assert self.agent is not None
                if not message.acknowledged and self.agent.forward_errors():
                    self.forward_error(message, conn, traceback.format_exc())
                else:
                    self.logger.exception(
                        f"An unexpected exception occurred while processing a message."
                    )

    def forward_error(self, message: Message, conn: Connection, stack: str) -> None:
        """When an unexpected error occurred while processing a message, it is
        forwarded to an error queue, defined in the global variable
        ``ERROR_QUEUE_NAME``.

        :param message: The RabbitMQ message associated with the error
        :type message: Message
        :param conn: An instance of ``Connection`` created by ``ConnectionManager.run()``
        :type conn: Connection
        :param stack: The python traceback of the error
        :type stack: str
        """
        body = json.loads(message.body.decode())
        # Parses message
        new_message = {
            "error": stack,
            "timestamp": datetime.utcnow().timestamp(),
            "original_message": body,
            "queue": self.queue_name,
        }
        # Get reply queue name and get the queue reference id not in index
        try:
            # Forwards message
            with conn.Producer(routing_key=ERROR_QUEUE_NAME) as producer:
                producer.publish(
                    json.dumps(new_message).encode(),
                    headers={"source-id": self.queue_name},
                )

            # Send ack
            message.ack()
            self.logger.error(
                "An error occurred and has been forwarded to the %s queue : \n%s"
                % (ERROR_QUEUE_NAME, stack)
            )

        except (ConsumerCancelled, ConnectionResetError, BrokenPipeError, OSError):
            # Reconnect
            return

        except:
            self.logger.exception(
                "An unexpected error occurred while forwarding message to error queue"
            )
            message.requeue()
            raise

    def stop(self) -> None:
        """Mark the execution loop to stop at next iteration."""
        self.stopped = True


class Runner:
    """Create sub-processes to listen to a queue and perform some work.

    :param queue_name: The name of the queue to listen.
    :type queue_name: str
    :param agent_class: An ``Agent`` object (not an instance)
    :type agent_class: Type[Agent]
    :param extra_conf_properties: Additional properties, defaults to None
    :type extra_conf_properties: dict, optional
    """

    def __init__(
        self,
        queue_name: str,
        agent_class: Type[Agent],
        extra_conf_properties: Optional[dict] = None,
    ):
        # Parse command line
        self.n_processes, self.conf = self.parse_cli(extra_conf_properties)
        self.queue_name = queue_name
        self.processes: Dict[int, Process] = {}
        self.agent_class = agent_class

        # Instantiating sub-logger
        self.logger = initialize_logger("runner")

    def parse_cli(
        self, extra_conf_properties: Optional[dict] = None
    ) -> Tuple[int, dict]:
        """Parse the cli argument ``--proc``, which sets the number of ``Agent`` sub-processes
        to initialize. Also calls ``get_conf_schema`` to get optional additional configuration.


        :param extra_conf_properties: a dict of additional properties, defaults to None
        :type extra_conf_properties: dict, optional
        :return: number of processes, additional properties
        :rtype: Tuple[int, dict]
        """
        parser = argparse.ArgumentParser(description="Starts an agent")
        parser.add_argument(
            "--proc",
            type=int,
            nargs="?",
            help="The number of processes to start (1 if missing)",
        )
        parser.add_argument("conf", help="Path to a json config file")
        args = parser.parse_args()

        n_processes = 1 if args.proc is None else args.proc

        with open(args.conf) as fd:
            conf = json.load(fd)

        validate(instance=conf, schema=Runner.get_conf_schema(extra_conf_properties))

        return n_processes, conf

    @staticmethod
    def get_conf_schema(extra_conf_properties: Optional[Dict] = None) -> Dict[str, Any]:
        """Parse the contents of the optional ``extra_conf_properties`` dict 

        :param extra_conf_properties: a dict of additional properties, defaults to None
        :type extra_conf_properties: dict, optional
        :return: A formatted dictionary containing the additional properties
        :rtype: Dict[str, Any]
        """
        if extra_conf_properties is None:
            return CONF_SCHEMA
        return {
            "properties": {
                **CONF_SCHEMA["properties"],
                **extra_conf_properties.get("properties", {}),
            },
            "required": CONF_SCHEMA.get("required", [])
            + extra_conf_properties.get("required", []),
        }

    def run(self) -> None:
        """Start sub-processes and wait forever for their termination."""
        # Spawning processes
        for i in range(0, self.n_processes):
            manager = ConnectionManager(
                queue_name=self.queue_name,
                agent_class=self.agent_class,
                conf=self.conf,
                process_id=i,
            )
            manager.start()
            self.processes[i] = manager
            self.logger.info("launching [%d]" % i)

        # Now waiting for subscriptions to die (should not happen)
        for i in self.processes:
            self.processes[i].join()

        self.logger.warning("Ended all of %d processes." % len(self.processes))
