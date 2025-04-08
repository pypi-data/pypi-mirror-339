# Queue Updater

A simple Python package for updating queue items in a Django service.

## Installation

```bash
pip install anzu
```

## Usage

### Using the QueueClient class (recommended)

```python
from anzu import QueueClient

# Initialize with explicit parameters
client = QueueClient(
    django_url="https://your-django-service.com",
    username="admin",
    password="password",
    service_endpoint="/api/queue/"
)

# Update a queue item
client.update_queue_item(
    qi_hash="abc123",
    status="completed",
    data={"result": "success"}
)

# Or initialize using environment variables
import os

os.environ["DJANGO_URL"] = "https://your-django-service.com"
os.environ["DJANGO_SUPERUSER_USERNAME"] = "admin"
os.environ["DJANGO_SUPERUSER_PASSWORD"] = "password"
os.environ["SERVICE_ENDPOINT"] = "/api/queue/"

client = QueueClient()
client.update_queue_item("abc123", "completed")
```

### Using the legacy function (for backward compatibility)

```python
import os
from anzu import update_queue_item

# Set required environment variables
os.environ["DJANGO_URL"] = "https://your-django-service.com"
os.environ["DJANGO_SUPERUSER_USERNAME"] = "admin"
os.environ["DJANGO_SUPERUSER_PASSWORD"] = "password"
os.environ["SERVICE_ENDPOINT"] = "/api/queue/"

# Update a queue item
update_queue_item(
    qi_hash="abc123",
    status="completed",
    data={"result": "success"}
)
```

## Environment Variables

- `DJANGO_URL`: URL of the Django service
- `DJANGO_SUPERUSER_USERNAME`: Django superuser username
- `DJANGO_SUPERUSER_PASSWORD`: Django superuser password
- `SERVICE_ENDPOINT`: Service endpoint (defaults to '/')

## License

MIT