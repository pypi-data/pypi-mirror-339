# Digital.ai Release Python API Stubs

The **Digital.ai Release Python API Stubs** (`digitalai-release-api-stubs`) provide Python stubs for interacting with the Digital.ai Release REST API.  
These stubs are generated using the **OpenAPI Generator**.

**Note:** Previously, these stubs were included as part of the `digitalai-release-sdk` version 24.1.0. They are now distributed as a separate package.

⚠️ **WARNING:**  
This project generates stubs for the **Digital.ai Release 23.3.0 API** and is **no longer being maintained**.

## 📦 Installation
Install the package using `pip`:

```sh
pip install digitalai-release-api-stubs
```

## 🚀 Getting Started

### Example Task: `message.py`

The example below demonstrates how to create a simple task that sets a system message in the Release UI using the API stubs.

```python
from digitalai.release.integration import BaseTask
from digitalai.release.v1.api_client import ApiClient
from digitalai.release.v1.configuration import Configuration
from digitalai.release.v1.api.configuration_api import ConfigurationApi
from digitalai.release.v1.model.system_message_settings import SystemMessageSettings


class SetSystemMessage(BaseTask):
    """
        Sets the system message in the Release UI by invoking the API.
        Preconditions:
            - The 'Run as user' property must be set on the release.
            - The executing user should have valid credentials.
    """

    def execute(self) -> None:
        # Get the message from the input properties
        message = self.input_properties['message']

        # Create a configuration object
        configuration = Configuration(
            host=self.get_release_server_url(),
            username=self.get_task_user().username,
            password=self.get_task_user().password)

        # Instantiate the API client using the configuration above
        apiclient = ApiClient(configuration)

        # Create a client for the Configuration API using the API client
        configuration_api = ConfigurationApi(apiclient)

        # Prepare the system message payload with required fields
        system_message = SystemMessageSettings(
            type='xlrelease.SystemMessageSettings',
            id='Configuration/settings/SystemMessageSettings',
            message=message,
            enabled=True,
            automated=False
        )

        # Make the actual rest call to the designated endpoint
        configuration_api.update_system_message(system_message_settings=system_message)

        # Add a line to the comment section in the UI
        self.add_comment(f"System message updated to \"{message}\"")
```
## 🔁 Upgrading from `digitalai-release-sdk` 24.1.0 or 23.3.0 to 25.1.0

With the release of **digitalai-release-sdk 25.1.0**, the API stubs have been separated into a standalone package. 

To upgrade your project, follow these steps:

### Step 1: Install the API Stubs Package

You must explicitly install the new API stubs package:

```bash
pip install digitalai-release-api-stubs==25.1.0
```

Or, add it to your `requirements.txt` as needed.

---

### Step 2: Update Your Code

In previous versions, API clients were created like this:

```python
# Old code (pre-25.1.0)
configuration_api = ConfigurationApi(self.get_default_api_client())
```

In version **25.1.0**, use the following approach:

```python
# New code (25.1.0)

# Create a configuration object
configuration = Configuration(
    host=self.get_release_server_url(),
    username=self.get_task_user().username,
    password=self.get_task_user().password
)

# Instantiate the API client using the configuration
apiclient = ApiClient(configuration)

# Create the Configuration API client
configuration_api = ConfigurationApi(apiclient)
```

This pattern should be used for all API clients, such as `TemplateApi`, `TaskApi`, etc.

---

## 🔗 Related Resources

- 🧪 **Python Template Project**: [release-integration-template-python](https://github.com/digital-ai/release-integration-template-python)  
  A starting point for building custom integrations using Digital.ai Release and Python.

- 📦 **Digital.ai Release Python SDK**: [digitalai-release-sdk on PyPI](https://pypi.org/project/digitalai-release-sdk/)  
  The official SDK package for integrating with Digital.ai Release.
