class QueueUpdaterError(Exception):
    """Base exception for queue updater."""
    pass


class QueueUpdateError(QueueUpdaterError):
    """Exception raised when updating a queue item fails."""
    def __init__(self, status_code, response_text=None):
        self.status_code = status_code
        self.response_text = response_text
        message = f"Failed to update queue item. Status Code: {status_code}"
        if response_text:
            message += f", Response: {response_text}"
        super().__init__(message)