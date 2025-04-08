# Coiote Python

`python-coiote` is a Python package providing access to the Coiote DM server API. It supports `v3` Coiote DM API.

If you spot an issue, have a feature request or would like to discuss anything else, you're welcome to join [Coiote Discord community](https://discord.avsystem.com/).


## Features

`python-coiote` enables you to:

- interact with Coiote DM `v3` API to manage your devices, groups and domains,
- automatically URL-encode path parameters whenever needed,
- convert API responses to convenient Python data classes,
- conveniently deal with batch/paginated responses from `v3` API,
- handle authentication errors and retries,

and more.

## Installation

`python-coiote` is compatible with Python `>= 3.7`.

Use pip to install the latest stable version of `python-coiote`:

```bash
pip install --upgrade python-coiote
```

## Authentication

There are two ways of authenticating in Coiote API when using this SDK:

- Using credentials to your Coiote account:

```
from coiote.auth import Credentials
from coiote.client import Coiote


client = Coiote(url="https://eu.iot.avsystem.cloud", auth=Credentials("<your-username>", "<your-password>")) 
```

Since Coiote does not support generating API tokens yet, preferably, you should create a separate account in your Coiote
domain
that will have the permissions only to access the API endpoints you intend to use.

- Using a raw token acquired manually using the `oauth` endpoint in v3 API:

```
from coiote.client import Coiote

client = Coiote(url="https://eu.iot.avsystem.cloud", auth="<your-token>") 
```

## Using device client

`python-coiote` comes with builtin high level client designed for accessing specific device and to do so, composes
multiple API calls.
To read more, see [Device Client class](src/coiote/device_client.py). The device client supports a set of basic
operations:

```python3
client = Coiote(url="https://eu.iot.avsystem.cloud", auth="<token>")
endpoint_name = "device_name"
device = client.create_device_client(endpoint_name)
```

Get the whole datamodel or its parts:

```python3
device.get_all_data()
device.get_resource_value("Device.0.Timezone")
```

Schedule writing value to device's data model (it's async, method returns task ID):

```python3
write_task_id = device.write_to_resource("Device.0.Timezone", "Kraków/Radzikowskiego")
```

Schedule reading value from the actual device into its data model (it's async, method returns task ID):

```python3
read_task_id = device.read_resource("Device.0.Timezone")
```

Manually schedule executing a resource on a device (it's async, method returns task ID):

```python3
execute_task_id = device.execute_resource("Device.0.Reboot")
```

Schedule reboot of the device (it's async, method returns task ID):

```python3
reboot_task_id = device.reboot_device()
```

Get recently reported location:

```python3
device.get_location()
```

Access the device historical data - only for resources from objects with ID > 502:

```python3
from datetime import datetime, timedelta

start_time = datetime.now() - timedelta(minutes=15)
end_time = datetime.now()
data = c.device_monitoring.get_data_batch(endpoint_name, lwm2m_url="/3303/0/5700", start_time=start_time, end_time=end_time)
```

Download device data from given time range and save it to CSV using pandas:

```
import pandas as pd
from datetime import datetime, timedelta

device_id = "<enter device ID or endpointname>"
url = "<enter resource URL>"

# Pick last 30 days 
start_time = datetime.now() - timedelta(days=30)

# Download data
data = c.device_monitoring.get_all_data(device_id, lwm2m_url=url, start_time=start_time)

# Map data to Pandas dataframe and save it to CSV
data = {"value": [datapoint.value for datapoint in data],
        "datetime": [datapoint.date for datapoint in data]}
df = pd.DataFrame(data)
df.to_csv("<enter CSV file name>.csv")
```
