import logging
import os
import sys

from concurrent_log_handler import ConcurrentRotatingFileHandler


def initialize_logger(logger_name: str, log_file: str = None, log_level: int = logging.DEBUG,
                      log_rotate_max_size: int = 1024 * 1000 * 50, log_rotate_count: int = 5) -> logging.Logger:
    """
    Initialize loggers.
    :param logger_name: The logger name.
    :param log_file: The path to the log file.
    :param log_level:  The desired log level.
    :param log_rotate_max_size: The max size in bytes of an individual log file.
    :param log_rotate_count: The number of log files to keep.
    :return:
    """
    logger = logging.getLogger(logger_name)
    
    logger.propagate = False

    logger.setLevel(log_level)

    if log_file is None:
        if os.path.exists('/log'):
            # If we are running inside a container, let's put the logs in the /log dir.
            log_file = '/log/agent.txt'
        else:
            # Otherwise, we put them in the current directory
            log_file = '%s/log/agent.txt' % os.getcwd()

    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    # Define formatter
    formatter = logging.Formatter(
        '[%(name)-10s][%(levelname)-5s] %(asctime)s - %(message)s')

    # Define handlers

    # Since we can have multiple process running, we need a process-safe logger.
    file_handler = ConcurrentRotatingFileHandler(
        log_file, backupCount=log_rotate_count, maxBytes=log_rotate_max_size)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    logger.addHandler(file_handler)

    # Stdout logger is useful since it can been seen with docker logs
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)

    return logger
