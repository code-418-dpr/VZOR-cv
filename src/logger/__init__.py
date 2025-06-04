import logging

from src.logger._setup_logger import setup_logger

setup_logger()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


__all__ = ["get_logger"]
