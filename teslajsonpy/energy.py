#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Callable

from teslajsonpy.const import DEFAULT_ENERGYSITE_NAME, RESOURCE_TYPE

_LOGGER = logging.getLogger(__name__)


class EnergySite:
    """Base class to represents a Tesla energy site."""

    def __init__(self, api: Callable, energysite: dict, site_config: dict) -> None:
        """Initialize EnergySite."""
        self._api = api
        self._energysite = energysite
        self._site_config = site_config

    @property
    def energysite_id(self) -> int:
        """Return energy site id (aka site_id)."""
        return self._energysite.get("energy_site_id")

    @property
    def has_load_meter(self) -> bool:
        """Return True if energy site has a load meter."""
        return self._energysite.get("components", {}).get("load_meter")

    @property
    def has_battery(self) -> bool:
        """Return True if energy site has battery."""
        return self._energysite.get("components", {}).get("battery")

    @property
    def has_solar(self) -> bool:
        """Return True if energy site has solar."""
        return self._energysite.get("components", {}).get("solar")

    @property
    def id(self) -> str:
        # pylint: disable=invalid-name
        """Return battery_id."""
        return self._energysite.get("id")

    @property
    def resource_type(self) -> str:
        """Return energy site type."""
        return self._energysite[RESOURCE_TYPE]

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ) -> dict:
        """Wrap commands sent to Tesla API."""
        _LOGGER.debug("Sending command: %s", name)
        data = await self._api(
            name, path_vars=path_vars, wake_if_asleep=wake_if_asleep, **kwargs
        )
        _LOGGER.debug("Response from command %s: %s", name, data)
        return data


class SolarSite(EnergySite):
    """Represents a Tesla Energy Solar site.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energysite_objects`.
    """

    def __init__(
        self, api: Callable, energysite: dict, site_config: dict, site_data: dict
    ) -> None:
        """Initialize SolarSite."""
        super().__init__(api, energysite, site_config)
        self._site_data = site_data

    @property
    def data_available(self) -> bool:
        """Return if data is available."""
        return self._site_data != {}

    @property
    def grid_power(self) -> float:
        """Return grid power in Watts."""
        return self._site_data.get("grid_power")

    @property
    def load_power(self) -> float:
        """Return load power in Watts."""
        return self._site_data.get("load_power")

    @property
    def site_name(self) -> str:
        """Return energy site name."""
        # "site_name" not a valid key if name never set in Tesla app
        return self._site_config.get("site_name", DEFAULT_ENERGYSITE_NAME)

    @property
    def solar_power(self) -> float:
        """Return solar power in Watts."""
        return self._site_data.get("solar_power")

    @property
    def solar_type(self) -> str:
        """Return type of solar (e.g. pv_panels or roof)."""
        return self._energysite.get("components", {}).get("solar_type")


class PowerwallSite(EnergySite):
    """Represents a Tesla Energy Powerwall site.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energysite_objects`.
    """

    def __init__(
        self,
        api: Callable,
        energysite: dict,
        site_config: dict,
        site_data: dict,
        site_summary: dict,
    ) -> None:
        """Initialize PowerwallSite."""
        super().__init__(api, energysite, site_config)
        self._site_data: dict = site_data
        self._site_summary: dict = site_summary

    @property
    def backup_reserve_percent(self) -> int:
        """Return backup reserve percentage."""
        return self._site_config.get("backup_reserve_percent")

    @property
    def battery_power(self) -> float:
        """Return battery power in Watts."""
        return self._site_summary.get("battery_power")

    @property
    def data_available(self) -> bool:
        """Return if data is available."""
        return self._site_summary != {}

    @property
    def energy_left(self) -> float:
        """Return battery energy left in Watt hours."""
        return round(self._site_config.get("nameplate_energy", 0) * self.percentage_charged / 100)

    @property
    def grid_power(self) -> float:
        """Return grid power in Watts."""
        return self._site_data.get("grid_power")

    @property
    def grid_status(self) -> str:
        """Return grid status."""
        return self._site_data.get("grid_status")

    @property
    def load_power(self) -> float:
        """Return load power in Watts."""
        return self._site_data.get("load_power")

    @property
    def operation_mode(self) -> str:
        """Return operation mode."""
        return self._site_config.get("default_real_mode")

    @property
    def percentage_charged(self) -> float:
        """Return battery percentage charged."""
        # percentage_charged sometimes incorrectly reports 0
        return self._site_summary.get("percentage_charged", 0)

    @property
    def site_name(self) -> str:
        """Return energy site name."""
        # "site_name" not a valid key if name never set in Tesla app
        return self._site_summary.get("site_name", DEFAULT_ENERGYSITE_NAME)

    @property
    def solar_power(self) -> float:
        """Return solar power in Watts."""
        return self._site_data.get("solar_power")

    @property
    def version(self) -> float:
        """Return firmware version."""
        return self._site_config.get("version")

    async def set_operation_mode(self, real_mode: str) -> None:
        """Set operation mode of Powerwall.

        Mode: "self_consumption", "backup", "autonomous"
        """
        data = await self._send_command(
            "BATTERY_OPERATION_MODE",
            path_vars={"site_id": self.energysite_id},
            default_real_mode=real_mode,
        )
        if data:
            response = data.get("response", {})
            # Find 'code' key case-insensitively
            code = next((v for k, v in response.items() if k.lower() == "code"), None)
            if code == 201:
                self._site_config.update({"operation": real_mode})

    async def set_reserve_percent(self, value: int) -> None:
        """Set reserve percentage of Powerwall.

        Value: 0-100
        """
        data = await self._send_command(
            "BACKUP_RESERVE",
            path_vars={"site_id": self.energysite_id},
            backup_reserve_percent=int(value),
        )
        if data:
            response = data.get("response", {})
            # Find 'code' key case-insensitively
            code = next((v for k, v in response.items() if k.lower() == "code"), None)
            if code == 201:
                self._site_config.update({"backup_reserve_percent": value})


class SolarPowerwallSite(PowerwallSite):
    """Represents a Tesla Energy Solar site with Powerwall(s).

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energysite_objects`.
    """

    @property
    def export_rule(self) -> str:
        """Return energy export rule setting."""
        return self._site_config.get("components", {}).get(
            "customer_preferred_export_rule"
        )

    @property
    def grid_charging(self) -> bool:
        """Return grid charging."""
        # Key is missing from site config when False
        return not self._site_config.get("components", {}).get(
            "disallow_charge_from_grid_with_solar_installed", False
        )

    @property
    def solar_type(self) -> str:
        """Return type of solar (e.g. pv_panels or roof)."""
        return self._site_config.get("components", {}).get("solar_type")

    async def set_grid_charging(self, value: bool) -> None:
        """Set grid charging setting of Powerwall."""
        value = not value
        await self._send_command(
            "ENERGY_SITE_IMPORT_EXPORT_CONFIG",
            path_vars={"site_id": self.energysite_id},
            disallow_charge_from_grid_with_solar_installed=value,
        )
        # This endpoint returns an empty response instead of a result code
        self._site_config["components"].update(
            {"disallow_charge_from_grid_with_solar_installed": value}
        )

    async def set_export_rule(self, setting: str) -> None:
        """Set energy export setting of Powerwall.

        Settings
          Solar: "pv_only"
          Everything: "battery_ok"
        """
        await self._send_command(
            "ENERGY_SITE_IMPORT_EXPORT_CONFIG",
            path_vars={"site_id": self.energysite_id},
            customer_preferred_export_rule=setting,
        )
        # This endpoint returns an empty response instead of a result code
        self._site_config["components"].update(
            {"customer_preferred_export_rule": setting}
        )
