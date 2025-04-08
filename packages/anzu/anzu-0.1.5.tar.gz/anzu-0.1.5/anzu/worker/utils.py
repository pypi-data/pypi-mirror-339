import logging
import os


def get_env_var(name, default=None, required=False):
    """Get environment variable with proper error handling."""
    value = os.environ.get(name, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{name}' is not set")
    return value


def setup_logger(name='queue_updater', level=logging.INFO):
    """Setup and return a logger with the given name and level."""
    logger = logging.getLogger(name)

    # Only add handler if not already added to avoid duplicate logs
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    return logger