import logging

logging.basicConfig(
    encoding="utf-8",
    level="INFO",
    filemode="w",
    format="%(name)s [%(asctime)s] %(levelname)s %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

__all__ = ["get_logger"]
