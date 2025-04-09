"""
Sensors module for sensor configuration and data.

This module provides classes for configuring and reading data from sensors.
"""

from instinct_py.headset.sensors.manager import HeadsetSensorsManager
from instinct_py.headset.sensors.types import (
    SensorConfig,
    SensorData,
    SensorResponse,
)

__all__ = [
    "HeadsetSensorsManager",
    "SensorConfig",
    "SensorData",
    "SensorResponse",
]
