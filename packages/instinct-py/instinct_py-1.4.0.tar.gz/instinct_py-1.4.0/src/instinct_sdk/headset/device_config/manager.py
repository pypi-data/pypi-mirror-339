"""
Device configuration manager module.

This module provides the DeviceConfigManager class for storing and retrieving
persistent configuration values on the headset.
"""

from typing import Any, Dict, List, Optional, Union

from instinct_sdk.headset.configuration.base import HeadsetSystemConfiguration
from instinct_sdk.headset.device_config.types import (
    DeviceConfig,
    DeviceConfigResponse,
)
from instinct_sdk.utils.http_client import HttpClient


class DeviceConfigManager:
    """Manages device configuration storage.

    Provides methods for creating, retrieving, updating, and deleting
    configuration entries on the headset.

    Parameters
    ----------
    headset : Any
        The parent Headset instance
    """

    def __init__(self, headset: Any) -> None:
        """Initialize the device configuration manager.

        Parameters
        ----------
        headset : Any
            The parent Headset instance
        """
        self._headset = headset
        self._http_client = HttpClient()
        self._system_configuration = HeadsetSystemConfiguration(
            headset.base_configuration
        )
        self._device_config_base_url = (
            f"{self._system_configuration.base_configuration.system_base}/config"
        )

    def create_config(
        self, config_data: Union[Dict[str, Any], DeviceConfig]
    ) -> DeviceConfig:
        """Create a new configuration entry.

        Parameters
        ----------
        config_data : Union[Dict[str, Any], DeviceConfig]
            The configuration data to store

        Returns
        -------
        DeviceConfig
            The created configuration entry

        Raises
        ------
        Exception
            If the request fails

        Examples
        --------
        >>> # Store user preferences
        >>> config = headset.device_config_manager.create_config({
        ...     "key": "userPreference.theme",
        ...     "value": "dark"
        ... })
        >>>
        >>> # Store temporary data with expiration
        >>> config = headset.device_config_manager.create_config({
        ...     "key": "session.authToken",
        ...     "value": "abc123xyz",
        ...     "expires_in": "1h"
        ... })
        """
        # Convert to DeviceConfig if it's a dict
        if isinstance(config_data, dict):
            config = DeviceConfig(**config_data)
        else:
            config = config_data

        try:
            response = self._http_client.post(
                self._device_config_base_url,
                json=config.model_dump(),
            )
            return DeviceConfig.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't create configuration. {error}")

    def get_config(self, key: str) -> DeviceConfig:
        """Retrieve a configuration by key.

        Parameters
        ----------
        key : str
            The key of the configuration to retrieve

        Returns
        -------
        DeviceConfig
            The retrieved configuration entry

        Raises
        ------
        Exception
            If the request fails or the configuration doesn't exist

        Examples
        --------
        >>> # Retrieve a configuration
        >>> config = headset.device_config_manager.get_config("userPreference.theme")
        >>> print(f"Theme preference: {config.value}")
        """
        try:
            response = self._http_client.get(
                f"{self._device_config_base_url}/{key}",
            )
            return DeviceConfig.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't get configuration for key '{key}'. {error}")

    def list_configs(self) -> List[DeviceConfig]:
        """List all configurations.

        Returns
        -------
        List[DeviceConfig]
            All configuration entries

        Raises
        ------
        Exception
            If the request fails

        Examples
        --------
        >>> # List all configurations
        >>> configs = headset.device_config_manager.list_configs()
        >>> for config in configs:
        ...     print(f"{config.key}: {config.value}")
        """
        try:
            response = self._http_client.get(self._device_config_base_url)
            return [DeviceConfig.model_validate(item) for item in response]
        except Exception as error:
            raise Exception(f"Couldn't list configurations. {error}")

    def update_config(
        self, key: str, config_data: Union[Dict[str, Any], DeviceConfig]
    ) -> DeviceConfig:
        """Update an existing configuration.

        Parameters
        ----------
        key : str
            The key of the configuration to update
        config_data : Union[Dict[str, Any], DeviceConfig]
            The new configuration data

        Returns
        -------
        DeviceConfig
            The updated configuration entry

        Raises
        ------
        Exception
            If the request fails or the configuration doesn't exist

        Examples
        --------
        >>> # Update a configuration
        >>> updated_config = headset.device_config_manager.update_config(
        ...     "userPreference.theme",
        ...     {
        ...         "key": "userPreference.theme",
        ...         "value": "light"
        ...     }
        ... )
        """
        # Convert to DeviceConfig if it's a dict
        if isinstance(config_data, dict):
            config = DeviceConfig(**config_data)
        else:
            config = config_data

        try:
            response = self._http_client.put(
                f"{self._device_config_base_url}/{key}",
                json=config.model_dump(),
            )
            return DeviceConfig.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't update configuration for key '{key}'. {error}")

    def delete_config(self, key: str) -> DeviceConfigResponse:
        """Delete a configuration entry.

        Parameters
        ----------
        key : str
            The key of the configuration to delete

        Returns
        -------
        DeviceConfigResponse
            Response from the delete operation

        Raises
        ------
        Exception
            If the request fails or the configuration doesn't exist

        Examples
        --------
        >>> # Delete a configuration
        >>> response = headset.device_config_manager.delete_config("session.authToken")
        >>> if response.success:
        ...     print("Configuration deleted successfully")
        """
        try:
            response = self._http_client.delete(
                f"{self._device_config_base_url}/{key}",
            )
            return DeviceConfigResponse.model_validate(response)
        except Exception as error:
            raise Exception(f"Couldn't delete configuration for key '{key}'. {error}")
