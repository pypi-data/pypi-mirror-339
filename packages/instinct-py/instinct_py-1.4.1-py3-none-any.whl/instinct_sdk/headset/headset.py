"""
Core module for interacting with Nexstem Instinct headsets.

This module contains the main Headset class that serves as the primary entry point
for discovering, connecting to, and controlling Instinct headsets.
"""

import socket
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from instinct_sdk.headset.configuration.base import (
    HeadsetBaseConfiguration,
    HeadsetSystemConfiguration,
)
from instinct_sdk.headset.device_config.manager import DeviceConfigManager
from instinct_sdk.headset.electrode.manager import HeadsetElectrodesManager
from instinct_sdk.headset.sensors.manager import HeadsetSensorsManager
from instinct_sdk.headset.stream.manager import HeadsetStreamsManager
from instinct_sdk.utils.http_client import HttpClient


class DebugCommand(BaseModel):
    """Debug command interface for low-level hardware interaction.

    Used for sending direct commands to headset peripherals.
    """

    cmd_resp: int
    peripheral: int
    peripheral_channels: int
    parameter: List[int]
    data: List[int]
    packet_type: int


class HeadsetBattery(BaseModel):
    """Battery status and information for the headset."""

    has_battery: bool
    cycle_count: int
    is_charging: int
    designed_capacity: int
    max_capacity: int
    current_capacity: int
    voltage: int
    percent: int
    capacity_unit: str
    time_remaining: int
    ac_connected: bool
    type: str
    model: str
    manufacturer: str
    serial: str


class HeadsetCPU(BaseModel):
    """CPU status and information for the headset."""

    load: int
    temperature: int
    total_clock_speed: int
    current_clock_speed: int


class HeadsetRAM(BaseModel):
    """RAM status and information for the headset."""

    total: int
    available: int
    free: int


class HeadsetStorage(BaseModel):
    """Storage status and information for the headset."""

    total: int
    free: int


class HeadsetState(BaseModel):
    """Comprehensive state information for the headset.

    Includes status, network configuration, and hardware metrics.
    """

    status: str
    http_port: int
    grpc_port: int
    host: str
    battery: HeadsetBattery
    cpu: HeadsetCPU
    ram: HeadsetRAM
    storage: HeadsetStorage


class HeadsetName(BaseModel):
    """Headset name information."""

    name: str


class HeadsetSetNameResponse(BaseModel):
    """Response for headset name setting operation."""

    message: str
    success: bool


@dataclass
class HeadsetConfig:
    """Configuration options for Headset initialization."""

    base_url: Optional[str] = None
    discovery_port: Optional[int] = None
    debug: bool = False
    services: Optional[Dict[str, str]] = None


class Headset:
    """The main Headset class representing an Instinct headset.

    Provides access to all headset functionality including streams, electrodes,
    and sensors. Serves as the primary entry point for the SDK.

    Parameters
    ----------
    host_address : str
        The IP address of the headset
    config : Optional[HeadsetConfig]
        Optional configuration parameters

    Attributes
    ----------
    host_address : str
        IP address of the headset
    base_configuration : HeadsetBaseConfiguration
        Base configuration for all services
    streams_manager : HeadsetStreamsManager
        Manager for creating and controlling streams
    electrode_manager : HeadsetElectrodesManager
        Manager for electrode configuration and data
    sensor_manager : HeadsetSensorsManager
        Manager for sensor configuration and data
    device_config_manager : DeviceConfigManager
        Manager for device configuration storage
    """

    def __init__(
        self, host_address: str, config: Optional[HeadsetConfig] = None
    ) -> None:
        """Initialize a Headset instance for direct connection to a known headset."""
        self.host_address = host_address

        # Set default config if none provided
        if config is None:
            config = HeadsetConfig()

        self._is_debug_enabled = config.debug

        # Initialize configuration objects with provided or default settings
        system_base = None
        streams_base = None
        if config.services:
            system_base = config.services.get("system")
            streams_base = config.services.get("streams")

        self.base_configuration = HeadsetBaseConfiguration(
            base_url=config.base_url, system_base=system_base, streams_base=streams_base
        )
        self._system_configuration = HeadsetSystemConfiguration(self.base_configuration)

        # Standard 10-20 EEG electrode positions
        standard_electrodes = [
            "PZ",
            "O1",
            "O2",
            "P3",
            "P4",
            "T5",
            "T6",
            "C3",
            "C4",
            "T3",
            "T4",
            "CMS",
            "DRL",
            "CZ",
            "F7",
            "F8",
            "F3",
            "F4",
            "FP1",
            "FP2",
            "FZ",
        ]

        # Initialize managers
        self.electrode_manager = HeadsetElectrodesManager(self, standard_electrodes)
        self.sensor_manager = HeadsetSensorsManager(self)
        self.device_config_manager = DeviceConfigManager(self)
        self.streams_manager = HeadsetStreamsManager(self)

        # Create HTTP client
        self._http_client = HttpClient()

    @property
    def streams_manager(self) -> HeadsetStreamsManager:
        """Manager for creating and controlling streams."""
        return self._streams_manager

    @streams_manager.setter
    def streams_manager(self, value: HeadsetStreamsManager) -> None:
        self._streams_manager = value

    @property
    def electrode_manager(self) -> HeadsetElectrodesManager:
        """Manager for electrode configuration and data."""
        return self._electrode_manager

    @electrode_manager.setter
    def electrode_manager(self, value: HeadsetElectrodesManager) -> None:
        self._electrode_manager = value

    @property
    def sensor_manager(self) -> HeadsetSensorsManager:
        """Manager for sensor configuration and data."""
        return self._sensor_manager

    @sensor_manager.setter
    def sensor_manager(self, value: HeadsetSensorsManager) -> None:
        self._sensor_manager = value

    @property
    def device_config_manager(self) -> DeviceConfigManager:
        """Manager for device configuration storage."""
        return self._device_config_manager

    @device_config_manager.setter
    def device_config_manager(self, value: DeviceConfigManager) -> None:
        self._device_config_manager = value

    @staticmethod
    def discover(
        timeout: int = 3000, discovery_port: int = 48010, debug: bool = False
    ) -> List["Headset"]:
        """Discover all Instinct headsets on the local network.

        Uses UDP broadcast to find headsets and returns instances for each one found.

        Parameters
        ----------
        timeout : int, optional
            Timeout in milliseconds for the discovery process, by default 3000
        discovery_port : int, optional
            Port to use for broadcasting discovery messages, by default 48010
        debug : bool, optional
            Whether to enable debug mode for discovered headsets, by default False

        Returns
        -------
        List[Headset]
            List of Headset instances for discovered headsets

        Raises
        ------
        Exception
            If there's a network error during the discovery process
        """
        discovered_devices: List[str] = []

        # Create broadcast and receive sockets
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Enable broadcasting
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            # Bind receive socket
            receive_socket.bind(("0.0.0.0", 0))
            receive_port = receive_socket.getsockname()[1]

            # Set non-blocking receive
            receive_socket.setblocking(False)

            # Format and send the discovery message
            message = f"INSTINCT_DISCOVER:{receive_port}".encode()
            broadcast_socket.sendto(message, ("255.255.255.255", discovery_port))

            # Wait for responses
            start_time = time.time()
            timeout_seconds = timeout / 1000

            while time.time() - start_time < timeout_seconds:
                try:
                    data, addr = receive_socket.recvfrom(1024)
                    if addr[0] not in discovered_devices:
                        discovered_devices.append(addr[0])
                except BlockingIOError:
                    # No data available, continue polling
                    time.sleep(0.1)

            # Create headset instances for each discovered device
            return [
                Headset(
                    device_ip,
                    HeadsetConfig(
                        base_url=f"http://{device_ip}:42069",
                        debug=debug,
                        discovery_port=discovery_port,
                    ),
                )
                for device_ip in discovered_devices
            ]

        finally:
            # Clean up sockets
            broadcast_socket.close()
            receive_socket.close()

    def send_debug_command(
        self, command: DebugCommand, timeout: int = 1000
    ) -> DebugCommand:
        """Send a debug command to the headset.

        Only available when debug mode is enabled.

        Parameters
        ----------
        command : DebugCommand
            The debug command to send
        timeout : int, optional
            Timeout in milliseconds for the request, by default 1000

        Returns
        -------
        DebugCommand
            Command response from the headset

        Raises
        ------
        ValueError
            If debug mode is not enabled
        Exception
            If the command fails
        """
        if not self._is_debug_enabled:
            raise ValueError("Debug mode is not enabled. Command failed.")

        try:
            response = self._http_client.post(
                self._system_configuration.url_headset_send_debug_command,
                data=command.model_dump(),
                timeout=timeout / 1000,
            )
            return DebugCommand.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't send debug command. {error}")

    def get_state(self, timeout: int = 1000) -> HeadsetState:
        """Get the current state of the headset.

        Includes information about status, battery, CPU, RAM, and storage.

        Parameters
        ----------
        timeout : int, optional
            Timeout in milliseconds for the request, by default 1000

        Returns
        -------
        HeadsetState
            Comprehensive state information for the headset

        Raises
        ------
        Exception
            If the request fails
        """
        try:
            response = self._http_client.get(
                self._system_configuration.url_headset_get_state,
                timeout=timeout / 1000,
            )
            return HeadsetState.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't get health of the headset. {error}")

    def get_name(self, timeout: int = 1000) -> str:
        """Get the current name of the headset.

        Parameters
        ----------
        timeout : int, optional
            Timeout in milliseconds for the request, by default 1000

        Returns
        -------
        str
            The name of the headset

        Raises
        ------
        Exception
            If the request fails
        """
        try:
            response = self._http_client.get(
                self._system_configuration.url_headset_get_name,
                timeout=timeout / 1000,
            )
            headset_name = HeadsetName.model_validate(response)
            return headset_name.name
        except Exception as error:
            raise Exception(f"Couldn't get name of the headset. {error}")

    def set_name(self, name: str, timeout: int = 0) -> HeadsetSetNameResponse:
        """Set a new name for the headset.

        Parameters
        ----------
        name : str
            The new name for the headset
        timeout : int, optional
            Timeout in milliseconds for the request (0 means no timeout), by default 0

        Returns
        -------
        HeadsetSetNameResponse
            Response from the name-setting operation

        Raises
        ------
        Exception
            If the request fails
        """
        try:
            response = self._http_client.patch(
                self._system_configuration.url_headset_set_name,
                data={"hostname": name},
                timeout=timeout / 1000 if timeout > 0 else None,
            )
            return HeadsetSetNameResponse.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't set name of the headset. {error}")
