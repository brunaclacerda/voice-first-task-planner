import logging

from .config import get_settings


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Sets up a logger.

    Parameters:
    name (str): The name of the logger.

    Returns:
    logging.Logger: Configured logger.
    """
    settings = get_settings()

    # Obtain a reference to the logger
    logger = logging.getLogger(name)

    # Check if the logger is already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    logger.setLevel(settings.log_level)
    return logger
