import logging


class AnzuLogger:
    _instance = None

    def __new__(cls, level: str = logging.INFO, name: str = __name__):
        # Ensures that only one instance of the logger is created
        if cls._instance is None:
            cls._instance = super(AnzuLogger, cls).__new__(cls)
            cls._instance._logger = logging.getLogger(name)
            cls._instance._logger.setLevel(logging.INFO)  # Default log level
            handler = logging.StreamHandler()  # You can also use FileHandler
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            cls._instance._logger.addHandler(handler)

        return cls._instance._logger

    def get_logger(self):
        """Returns the logger instance."""
        return self._instance._logger

    def set_name(self, name: str):
        """Sets the name of the logger."""
        self._instance._logger = logging.getLogger(name)

    def add_file_handler(self, file_name: str):
        """Adds a file handler to the logger."""
        handler = logging.FileHandler(file_name)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self._instance._logger.addHandler(handler)

    def remove_handler(self, handler):
        """Removes a handler from the logger."""
        self._instance._logger.removeHandler(handler)


logger = AnzuLogger()
redis_logger = AnzuLogger(name="redis_logger")
