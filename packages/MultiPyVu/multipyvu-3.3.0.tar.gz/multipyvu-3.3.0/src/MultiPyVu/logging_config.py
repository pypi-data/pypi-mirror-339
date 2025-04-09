'''
logging_config.py is used to hold methods to help with the logging module
'''

import logging.config
from logging import Logger
from os import path

import yaml

from .project_vars import LOG_NAME

NUMBER_OF_CALLS = 0


def absolute_path(filename: str) -> str:
    """
    Finds the absolute path of a file based on its location
    relative to the gui module

    Parameters:
    -----------
    filename: str
        The file location based on its relative path from the gui module
    """
    abs_path = path.abspath(
        path.join(path.dirname(
            __file__), './'))
    return path.join(abs_path, filename)


def setup_logging(display_logger_name: bool = True):
    global NUMBER_OF_CALLS

    # avoid calling this if the server and client
    # are being run on the same computer
    if NUMBER_OF_CALLS == 0:
        yaml_path = 'logging_config.yaml'
        abs_path = path.abspath(path.join(path.dirname(__file__), './'))
        yaml_path = path.join(abs_path, yaml_path)
        with open(yaml_path, 'r') as f:
            log_config = yaml.safe_load(f.read())

            # define variables
            log_config['handlers']['file']['filename'] = LOG_NAME
            if display_logger_name:
                formatter = 'show_name'
            else:
                formatter = 'no_name'
            log_config['handlers']['console']['formatter'] = formatter

            logging.config.dictConfig(log_config)
    NUMBER_OF_CALLS += 1


def remove_logs(logger: Logger) -> None:
    """
    Removes all references to handlers for the logger and closes the logger.

    Parameters:
    -----------
    logger: Logger
        The logging event to remove all handlers.
    """
    if logger is not None:
        while logger.hasHandlers():
            if len(logger.handlers) == 0:
                break
            else:
                for handler in logger.handlers:
                    handler.close()
                    logger.removeHandler(handler)
