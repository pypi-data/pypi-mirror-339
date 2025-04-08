import logging
import uuid

__all__ = ["get_logger", "get_nonce"]


def get_logger(name: str = "service") -> logging.Logger:
    return logging.getLogger(name)


def get_nonce() -> str:
    """Generate random 12 hexadecimal string

    :return: 12 hexadecimal char long string
    """
    return uuid.uuid4().hex[:12]
