"""
Device configuration module.

This module provides classes for storing and retrieving persistent configuration
values on the headset.
"""

from instinct_sdk.headset.device_config.manager import DeviceConfigManager
from instinct_sdk.headset.device_config.types import (
    DeviceConfig,
    DeviceConfigResponse,
)

__all__ = ["DeviceConfigManager", "DeviceConfig", "DeviceConfigResponse"]
