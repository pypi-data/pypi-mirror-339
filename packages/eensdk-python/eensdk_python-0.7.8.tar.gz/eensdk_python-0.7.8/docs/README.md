# een-python Package Documentation

## Overview

The `eensdk-python` package provides a Python client for interacting with the Eagle Eye Networks API. This package simplifies authentication, API calls, and utility tasks, enabling developers to quickly integrate their applications with the Eagle Eye Networks video platform.

## Installation

You can install the `eensdk-python` package using pip:

```bash
pip install eensdk-python
```

## Quick Start

### Before you Begin

To use this library, you will need to have a valid Eagle Eye Networks account and an application registered with the Eagle Eye Networks Developer Program. For more information on how to register an application, review the [API documentation](https://developer.eagleeyenetworks.com/docs/getting-started).

### Initialize the Client

To initialize the client, you will need to provide the following parameters:

- `client_id`: Your Eagle Eye Networks client ID.
- `client_secret`: Your Eagle Eye Networks client secret.
- `redirect_uri`: The URI to which the API redirects after authentication.

These parameters are can be obtained by registering an application with the Eagle Eye Networks Developer and [creating your client credentials](https://developer.eagleeyenetworks.com/docs/client-credentials).

You will also need to implement a token storage class that stores and retrieves access tokens. This class should implement the `TokenStorage` interface:

```python
from een import TokenStorage

class MyTokenStorage(TokenStorage):
    def get_token(self) -> str:
        # Retrieve the access token from your storage
        pass

    def set_token(self, token: str):
        # Store the access token in your storage
        pass

    def __contains__(self, key: str) -> bool:
        # Returns the token if it exists in your storage
        pass
```

Finally, initialize the client with your credentials and token storage:

```python
from een import EENClient, TokenStorage

token_storage = MyTokenStorage()
client = EENClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-redirect-uri",
    token_storage=token_storage
)
```

### Authentication

Authenticate with Eagle Eye Networks using the authorization code flow. For details on the authorization code flow, refer to the [Eagle Eye Networks API documentation](https://developer.eagleeyenetworks.com/docs/login-confidential-client).

```python
# Step 1: Get the authorization URL and direct users to it
print(client.get_auth_url())

# Step 2: Users will complete the authorization process and be redirected to your redirect URI. The authorization code will be included in the query parameters.
auth_code = request.args.get('code')
client.auth_een(auth_code, type="code")

# Step 3: The access token is now stored in your token storage. It will automatically be used for future requests.
client.list_cameras()

# You can also retrieve the access token directly through the TokenStorage interface
token = client.token_storage.get('access_token')
```

## Utilities

The `utils.py` module provides helpful functions for common tasks:

### Formatting Timestamps

The Eagle Eye Networks API requires timestamps in ISO 8601 format with millisecond precision. Use the `format_timestamp` function to convert timestamps to the required format:

```python
from een.utils import format_timestamp

formatted = format_timestamp("2025-01-01T12:00", user_timezone="America/New_York")
print(formatted)
```

### Generating Time Ranges

You can also generate timestamps for common time ranges, such as the previous seven days:

```python
from een.utils import get_timestamps
current, seven_days_ago = get_timestamps()
print(current, seven_days_ago)
```

### Converting camelCase to Title Case

Eagle Eye Networks often uses camelCase for identifiers such as event types or alert names. Use the `camel_to_title` function to convert these identifiers to a more readable title case.


```python
from een.utils import camel_to_title
converted = camel_to_title("motionDetected")
print(converted)  # Output: "Motion Detected"
```


## License

This package is provided under the MIT License.
