"""Configuration and logging utilities for rxvcapi"""
import os
import logging


class Config(object):
    """Configuration for RXVC"""

    def __init__(self, level=os.getenv('LOG_LEVEL', 'INFO')):
        self.valid_log_levels = [
            'CRITICAL',
            'ERROR',
            'WARNING',
            'INFO',
            'DEBUG',
            'NOTSET'
        ]

        self.log_level = self.validate_log_level(level)

    class ConfigException(Exception):
        pass

    def validate_log_level(self, level_s):
        """Validate that a user passed log level is a valid log level."""
        level_s = level_s.upper()
        if level_s in self.valid_log_levels:
            return getattr(logging, level_s)
        else:
            msg = "Valid values are: {}".format(
                ', '.join(self.valid_log_levels)
            )
            raise self.ConfigException(msg)

    def logger(self, name):
        """Returns a configured logger so we don't have to boilerplate it
        on every file.
        """
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        format_template = '%(asctime)s:%(name)s:%(levelname)s – %(message)s'

        handler.setFormatter(logging.Formatter(fmt=format_template,
                                            datefmt='%Y-%m-%d %H:%M:%S'))

        logger.setLevel(self.log_level)
        logger.addHandler(handler)

        return logger
