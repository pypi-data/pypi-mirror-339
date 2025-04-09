# Instinct SDK for Python

Python SDK for controlling and interacting with Nexstem Instinct headsets.

## Overview

The Instinct Python SDK provides a comprehensive set of tools for discovering, connecting to, and controlling Nexstem Instinct headsets from Python applications. This SDK enables developers to:

- Discover Instinct headsets on the local network
- Monitor headset state (battery, CPU, RAM, storage)
- Configure electrodes and sensors
- Create and manage data streams
- Build custom signal processing pipelines
- Store and retrieve device configuration values

## Installation

```bash
# Using pip
pip install instinct-sdk

# Using poetry
poetry add instinct-sdk
```

## Requirements

- Python 3.9 or later
- An Instinct headset on the same network

## Quick Start

### Discovering Headsets

```python
from instinct_sdk import Headset

# Discover all Instinct headsets on the network
headsets = Headset.discover()
print(f"Found {len(headsets)} headsets")

# Connect to the first headset found
headset = headsets[0]

# Or connect directly to a known headset
headset = Headset("192.168.1.100")
```

### Getting Headset State

```python
# Get basic headset information
state = headset.get_state()
print(f"Headset status: {state.status}")
print(f"Battery: {state.battery.percent}%")
print(f"CPU load: {state.cpu.load}%")

# Get the headset name
name = headset.get_name()
print(f"Headset name: {name}")
```

### Working with Streams

```python
import uuid

source_id = str(uuid.uuid4())
ssvep_id = str(uuid.uuid4())

# Create a stream
stream = headset.streams_manager.create_stream({
    "id": str(uuid.uuid4()),
    "nodes": [
        {
            "executable": "eeg_source",
            "config": {
                "sampleRate": 1000,
                "gain": 1,
            },
            "id": source_id,
        },
        {
            "executable": "ssvep_algo",
            "config": {},
            "id": ssvep_id,
        },
    ],
    "pipes": [
        {
            "source": source_id,
            "destination": ssvep_id,
        },
    ],
})

# Create the stream on the headset
await stream.create()

# Start the stream
await stream.start()

# Stop the stream when done
await stream.stop()
```

## API Documentation

### Headset Class

The main entry point for interacting with Instinct headsets.

#### Static Methods

| Method                                                              | Description                                |
| ------------------------------------------------------------------- | ------------------------------------------ |
| `Headset.discover(timeout=3000, discovery_port=48010, debug=False)` | Discovers Instinct headsets on the network |

#### Instance Properties

| Property                | Type                       | Description                                       |
| ----------------------- | -------------------------- | ------------------------------------------------- |
| `streams_manager`       | `HeadsetStreamsManager`    | Manager for creating and controlling data streams |
| `electrode_manager`     | `HeadsetElectrodesManager` | Manager for electrode configurations              |
| `sensor_manager`        | `HeadsetSensorsManager`    | Manager for sensor data                           |
| `device_config_manager` | `DeviceConfigManager`      | Manager for device configuration storage          |
| `host_address`          | `str`                      | IP address of the headset                         |

#### Instance Methods

| Method                        | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| `get_state()`                 | Gets the current state of the headset                  |
| `get_name()`                  | Gets the current name of the headset                   |
| `set_name(name)`              | Sets a new name for the headset                        |
| `send_debug_command(command)` | Sends a debug command to the headset (debug mode only) |

### Device Configuration Management

The SDK provides DeviceConfigManager for storing and retrieving persistent configuration values on the headset.

```python
# Store user preferences
await headset.device_config_manager.create_config({
    "key": "userPreference.theme",
    "value": "dark",
})

# Store temporary data with expiration
await headset.device_config_manager.create_config({
    "key": "session.authToken",
    "value": "abc123xyz",
    "expires_in": "1h",
})

# Retrieve configuration
config = await headset.device_config_manager.get_config("userPreference.theme")
print(f"Theme preference: {config.value}")

# Update configuration
await headset.device_config_manager.update_config(
    "userPreference.theme",
    {
        "key": "userPreference.theme",
        "value": "light",
    }
)

# Delete configuration
await headset.device_config_manager.delete_config("session.authToken")
```

### Stream Management

The SDK provides classes for creating and managing data processing streams:

```python
import uuid

# Create a stream with custom metadata
stream = headset.streams_manager.create_stream({
    "meta": {
        "name": "Alpha Rhythm Analysis",
        "description": "Extracts and analyzes alpha rhythms from occipital electrodes",
        "version": "1.0.0",
    },
    "nodes": [
        {
            "executable": "eeg_source",
            "config": {
                "sampleRate": 250,
                "channels": ["O1", "O2", "PZ"],
            },
        },
        {
            "executable": "bandpass_filter",
            "config": {
                "cutoff": 10,
                "bandwidth": 4,
                "order": 4,
            },
        },
    ],
    "pipes": [
        {
            "source": "source_id",
            "destination": "destination_id",
        },
    ],
})

# Create and start the stream
await stream.create()
await stream.start()

# Stop and delete the stream when done
await stream.stop()
await stream.delete()
```

### Electrode and Sensor Management

```python
# List all electrodes
electrodes = await headset.electrode_manager.list_electrodes()
for electrode in electrodes:
    print(f"{electrode.position}: {'enabled' if electrode.enabled else 'disabled'}")

# Enable an electrode
await headset.electrode_manager.enable_electrode("PZ")

# List all sensors
sensors = await headset.sensor_manager.list_sensors()
for sensor in sensors:
    print(f"{sensor.type}: {'enabled' if sensor.enabled else 'disabled'}")

# Enable the accelerometer
await headset.sensor_manager.enable_sensor("accelerometer", sample_rate=100)
```

## Error Handling

The SDK uses standard exception handling:

```python
try:
    headsets = Headset.discover()
    if len(headsets) == 0:
        print("No headsets found.")
        exit()

    headset = headsets[0]
    await headset.set_name("My Headset")
except Exception as error:
    print(f"Error: {error}")
```

## Troubleshooting

### Common Issues

1. **Cannot discover headsets**

   - Ensure the headset is powered on and connected to the same network
   - Check firewall settings that might block UDP broadcasts (port 48010)
   - Try specifying the IP address directly: `Headset("192.168.1.100")`

2. **Stream creation fails**

   - Verify all UUIDs are valid
   - Check that node executables exist on the headset
   - Ensure pipe connections reference valid node IDs

3. **Configuration storage fails**

   - Check that the key is a valid string
   - Ensure the value can be properly serialized
   - Verify that the expiration format is correct (e.g., "1h", "2d", "30m")

4. **Connection timeouts**
   - The headset may be overloaded; try simplifying your stream
   - Check network stability and latency
   - Increase timeout values in API calls

## Resources

- [Nexstem Developer Documentation](https://developers.nexstem.ai/)
- [Custom Nodes Tutorial](https://developers.nexstem.ai/tutorials/custom-nodes/overview)
- [API Reference](https://developers.nexstem.ai/api-reference/overview)
