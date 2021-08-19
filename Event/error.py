from eda_agent.utils import Agent
from kombu.message import Message
from typing import Dict, Any
from datetime import datetime
from kombu.transport.pyamqp import Channel

import os
import json

QUEUE_IN = 'ERROR_QUEUE'

EXTRA_CONFIG: Dict[str, Any] = {
    "properties": {
        "destination": {"type": "string"}
    },
    "required": []
}

DEFAULT_DESTINATION = "/errors"


class ErrorHandlingAgent(Agent):
    """
    Read message from ERROR_QUEUE and persist it for later analysis
    """

    def __init__(self, *args, **kwargs):
        super(ErrorHandlingAgent, self).__init__(*args, **kwargs)
        if self.conf.get("destination", None) is None:
            self.conf["destination"] = DEFAULT_DESTINATION

    @staticmethod
    def auto_ack():
        return True

    @staticmethod
    def forward_errors() -> bool:
        return False

    def parse_message(self, headers: dict, properties: dict, message: dict, raw_message: Message) -> None:
        """
        Reads a message from the error queue and persists it
        """
        try:
            self.logger.debug(
                f"Received error message from queue [{message['queue']}]")
            self.save_error(message)
        except:
            self.logger.exception(f"An exception occurred while processing an error message.\n{json.dumps(message, indent=2)}")
        finally:
            raw_message.ack()

    def save_error(self, message: dict):
        """
        Persist the error on local filesystem
        """
        if "timestamp" in message:
            timestamp = datetime.fromtimestamp(message["timestamp"]).isoformat()
        else:
            timestamp = datetime.now().isoformat()
        destination_dir = os.path.join(
            self.conf["destination"], message["queue"])
        # Make sure the directory exists
        os.makedirs(destination_dir, exist_ok=True)
        filename = f"{timestamp}.json"
        path = os.path.join(destination_dir, filename)
        with open(path, 'w') as f:
            json.dump(message, f, indent=2)
            self.logger.debug(f"Saved error message in [{path}]")
