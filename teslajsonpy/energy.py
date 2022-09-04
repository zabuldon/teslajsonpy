"""Tesla energy site."""
import logging
from typing import Callable

from teslajsonpy.const import (
    RESOURCE_TYPE,
    DEFAULT_ENERGYSITE_NAME,
)

_LOGGER = logging.getLogger(__name__)


class EnergySite:
    """Base class to represents a Tesla energy site."""

    def __init__(self, api: Callable, energysite: dict) -> None:
        """Initialize EnergySite."""
        self._api: Callable = api
        self._energysite: dict = energysite

    @property
    def energysite_id(self) -> int:
        """Return energy site id (aka site_id)."""
        return self._energysite.get("energy_site_id")

    @property
    def has_load_meter(self) -> bool:
        """Return True if energy site has a load meter."""
        return self._energysite.get("components").get("load_meter")

    @property
    def has_battery(self) -> bool:
        """Return True if energy site has battery."""
        return self._energysite.get("components").get("battery")

    @property
    def has_solar(self) -> bool:
        """Return True if energy site has solar."""
        return self._energysite.get("components").get("solar")

    @property
    def id(self) -> str:
        """Return id (aka battery_id)."""
        return self._energysite.get("id")

    @property
    def resource_type(self) -> str:
        """Return energy site type."""
        return self._energysite[RESOURCE_TYPE]

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ) -> dict:
        """Wrapper for sending commands to the Tesla API."""
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
        super().__init__(api, energysite)
        self._site_config: dict = site_config
        self._site_data: dict = site_data

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
        return self._energysite.get("components").get("solar_type")


class PowerwallSite(EnergySite):
    """Represents a Tesla Energy Powerwall site.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energysite_objects`.
    """

    def __init__(
        self, api: Callable, energysite: dict, battery_data: dict, battery_summary: dict
    ) -> None:
        """Initialize PowerwallSite."""
        super().__init__(api, energysite)
        self._battery_data: dict = battery_data
        self._battery_summary: dict = battery_summary

    @property
    def backup_reserve_percent(self) -> int:
        """Return backup reserve percentage."""
        return self._battery_data.get("backup").get("backup_reserve_percent")

    @property
    def battery_power(self) -> float:
        """Return battery power in Watts."""
        if self._battery_data.get("power_reading"):
            return self._battery_data["power_reading"][0]["battery_power"]

    @property
    def energy_left(self) -> float:
        """Return battery energy left in Watt hours."""
        return self._battery_summary.get("energy_left")

    @property
    def grid_power(self) -> float:
        """Return grid power in Watts."""
        if self._battery_data.get("power_reading"):
            return self._battery_data["power_reading"][0]["grid_power"]

    @property
    def grid_status(self) -> str:
        """Return grid status."""
        return self._battery_data.get("grid_status")

    @property
    def load_power(self) -> float:
        """Return load power in Watts."""
        if self._battery_data.get("power_reading"):
            return self._battery_data["power_reading"][0]["load_power"]

    @property
    def operation_mode(self) -> str:
        """Return operation mode."""
        return self._battery_data.get("operation")

    @property
    def percentage_charged(self) -> float:
        """Return battery percentage charged."""
        # percentage_charged sometimes incorrectly reports 0
        return self._battery_summary.get("percentage_charged")

    @property
    def site_name(self) -> str:
        """Return energy site name."""
        # "site_name" not a valid key if name never set in Tesla app
        return self._battery_data.get("site_name", DEFAULT_ENERGYSITE_NAME)

    @property
    def solar_power(self) -> float:
        """Return solar power in Watts."""
        if self._battery_data.get("power_reading"):
            return self._battery_data["power_reading"][0]["solar_power"]

    async def set_operation_mode(self, real_mode: str) -> None:
        """Set operation mode of Powerwall.

        Mode: "self_consumption", "backup", "autonomous"
        """
        data = await self._send_command(
            "BATTERY_OPERATION_MODE",
            path_vars={"battery_id": self.id},
            default_real_mode=real_mode,
        )
        if data and data["response"]["code"] == 201:
            self._battery_data.update({"operation": real_mode})

    async def set_reserve_percent(self, value: int) -> None:
        """Set reserve percentage of Powerwall.

        Value: 0-100
        """
        data = await self._send_command(
            "BACKUP_RESERVE",
            path_vars={"site_id": self.energysite_id},
            backup_reserve_percent=int(value),
        )
        if data and data["response"]["code"] == 201:
            self._battery_data["backup"].update({"backup_reserve_percent": value})


class SolarPowerwallSite(PowerwallSite):
    """Represents a Tesla Energy Solar site with Powerwall(s).

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energysite_objects`.
    """

    def __init__(
        self, api: Callable, energysite: dict, battery_data: dict, battery_summary: dict
    ) -> None:
        """Initialize SolarPowerwallSite."""
        super().__init__(api, energysite, battery_data, battery_summary)

    @property
    def export_rule(self) -> str:
        """Return energy export rule setting."""
        return self._battery_data["components"].get("customer_preferred_export_rule")

    @property
    def grid_charging(self) -> bool:
        """Return grid charging."""
        # Key is missing from battery_data when False
        return not self._battery_data["components"].get(
            "disallow_charge_from_grid_with_solar_installed", False
        )

    @property
    def solar_type(self) -> str:
        """Return type of solar (e.g. pv_panels or roof)."""
        return self._battery_data["components"].get("solar_type")

    async def set_grid_charging(self, value: bool) -> None:
        """Set grid charging setting of Powerwall."""
        value = not value
        await self._send_command(
            "ENERGY_SITE_IMPORT_EXPORT_CONFIG",
            path_vars={"site_id": self.energysite_id},
            disallow_charge_from_grid_with_solar_installed=value,
        )
        # This endpoint returns an empty response instead of a result code
        self._battery_data["components"].update(
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
        self._battery_data["components"].update(
            {"customer_preferred_export_rule": setting}
        )
