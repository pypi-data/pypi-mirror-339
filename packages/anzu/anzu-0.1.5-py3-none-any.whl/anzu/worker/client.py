import json
import requests
from requests.auth import HTTPBasicAuth
from .exceptions import QueueUpdateError
from .utils import get_env_var, setup_logger

logger = setup_logger()


class QueueClient:
    """Client for updating queue items in a Django service."""

    def __init__(self, django_url=None, username=None, password=None, service_endpoint=None, verify_ssl=None):
        """
        Initialize the queue client with connection parameters.

        Args:
            django_url (str, optional): URL of the Django service. Defaults to DJANGO_URL env var.
            username (str, optional): Django superuser username. Defaults to DJANGO_SUPERUSER_USERNAME env var.
            password (str, optional): Django superuser password. Defaults to DJANGO_SUPERUSER_PASSWORD env var.
            service_endpoint (str, optional): Service endpoint. Defaults to SERVICE_ENDPOINT env var or '/'.
            verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True unless URL contains 'https'.
        """
        self.django_url = django_url or get_env_var('DJANGO_URL', required=True)
        self.username = username or get_env_var('DJANGO_SUPERUSER_USERNAME', required=True)
        self.password = password or get_env_var('DJANGO_SUPERUSER_PASSWORD', required=True)
        self.service_endpoint = service_endpoint or get_env_var('SERVICE_ENDPOINT', '/')

        # Handle the verify_ssl parameter
        if verify_ssl is None:
            self.verify_ssl = False if 'https' in self.django_url else True
        else:
            self.verify_ssl = verify_ssl

        self.headers = {
            'Content-Type': 'application/json'
        }

    def update_queue_item(self, qi_hash, status, data=None, error=None, timeout=10):
        """
        Update a queue item with the given status and optional data or error.

        Args:
            qi_hash (str): Hash of the queue item to update.
            status (str): New status for the queue item.
            data (dict, optional): Additional data to update. Defaults to None.
            error (str, optional): Error message if applicable. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 10.

        Returns:
            dict: Response data from the API

        Raises:
            TypeError: If data is not a dictionary.
            QueueUpdateError: If the update request fails.
        """
        if not qi_hash:
            logger.warning("No queue item to update")
            return

        payload = {
            "status": status
        }

        if data is not None:
            if not isinstance(data, dict):
                raise TypeError(f"Expected dict, got {type(data)} with value: {data}")
            payload.update(data)

        if error is not None:
            payload['error'] = error

        url = f'{self.django_url}{self.service_endpoint}{qi_hash}/'

        response = requests.request(
            "PATCH",
            url,
            headers=self.headers,
            data=json.dumps(payload),
            auth=HTTPBasicAuth(self.username, self.password),
            verify=self.verify_ssl,
            timeout=timeout
        )

        if response.status_code not in [200, 204]:
            response_text = None
            if 'text/html' in response.headers.get('Content-Type', ''):
                logger.error(f"Failed to update queue item. Status Code: {response.status_code}")
            else:
                response_text = response.text
                logger.error(
                    f"Failed to update queue item. Status Code: {response.status_code}, Response: {response_text}")

            raise QueueUpdateError(response.status_code, response_text)

        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            # Return empty dict if no JSON in response
            return {}


# For backwards compatibility
def update_queue_item(qi_hash, status, data=None, error=None):
    """
    Legacy function to update a queue item. Uses environment variables for connection details.

    This function exists for backwards compatibility with the original code.
    New code should use the QueueClient class instead.
    """
    client = QueueClient()
    return client.update_queue_item(qi_hash, status, data, error)