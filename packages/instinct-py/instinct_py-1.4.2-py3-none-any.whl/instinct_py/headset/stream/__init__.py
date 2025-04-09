"""
Stream module for data processing streams.

This module provides classes for creating and managing data
processing streams on the headset.
"""

from instinct_py.headset.stream.manager import HeadsetStreamsManager
from instinct_py.headset.stream.node import Node
from instinct_py.headset.stream.pipe import Pipe
from instinct_py.headset.stream.stream import Stream
from instinct_py.headset.stream.types import (
    StreamConfig,
    StreamNodeConfig,
    StreamPipeConfig,
    StreamResponse,
    StreamSignal,
    NodeResponse,
    PipeResponse,
)

__all__ = [
    "HeadsetStreamsManager",
    "Node",
    "Pipe",
    "Stream",
    "StreamConfig",
    "StreamNodeConfig",
    "StreamPipeConfig",
    "StreamResponse",
    "StreamSignal",
    "NodeResponse",
    "PipeResponse",
]
