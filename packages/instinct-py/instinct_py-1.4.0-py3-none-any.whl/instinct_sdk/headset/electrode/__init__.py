"""
Electrode module for electrode configuration and data.

This module provides classes for configuring and reading data from electrodes.
"""

from instinct_sdk.headset.electrode.manager import HeadsetElectrodesManager
from instinct_sdk.headset.electrode.types import (
    ElectrodeConfig,
    ElectrodeData,
    ElectrodeResponse,
)

__all__ = [
    "HeadsetElectrodesManager",
    "ElectrodeConfig",
    "ElectrodeData",
    "ElectrodeResponse",
]
