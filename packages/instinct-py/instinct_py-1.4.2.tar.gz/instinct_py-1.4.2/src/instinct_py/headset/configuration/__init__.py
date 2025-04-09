"""
Configuration module for Instinct headset API URLs.

This module exports configuration classes for managing API URLs and endpoints.
"""

from instinct_py.headset.configuration.base import (
    HeadsetBaseConfiguration,
    HeadsetStreamsConfiguration,
    HeadsetSystemConfiguration,
)

__all__ = [
    "HeadsetBaseConfiguration",
    "HeadsetStreamsConfiguration",
    "HeadsetSystemConfiguration",
]
