"""Tesla Energy energy site."""

from teslajsonpy.const import (
    RESOURCE_TYPE,
    DEFAULT_ENERGY_SITE_NAME,
)


class EnergySite:
    """Base class to represents a Tesla Energy site."""

    def __init__(self, api, energysite, power_data) -> None:
        """Initialize EnergySite."""
        self._api = api
        self._energy_site = energysite
        self._power_data = power_data

    @property
    def energysite_id(self) -> int:
        """Return energy site id (aka site_id)."""
        return self._energy_site["energy_site_id"]

    @property
    def has_load_meter(self) -> int:
        """Return True if energy site has a load meter."""
        return self._energy_site["components"]["load_meter"]

    @property
    def id(self) -> int:
        """Return id (aka battery_id)."""
        return self._energy_site["id"]

    @property
    def resource_type(self) -> int:
        """Return energy site type."""
        return self._energy_site[RESOURCE_TYPE]

    @property
    def site_name(self) -> int:
        """Return energy site name."""
        # "site_name" not a valid key if name never set in Tesla app
        return self._energy_site.get("site_name", DEFAULT_ENERGY_SITE_NAME)


class SolarSite(EnergySite):
    """Represents a Tesla Energy Solar site.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energysite_objects`.
    """

    def __init__(self, api, energysite, power_data) -> None:
        """Initialize SolarSite."""
        super().__init__(api, energysite, power_data)

    @property
    def grid_power(self) -> int:
        """Return grid power in Watts."""
        # Add check to see if site has power metering?
        return self._power_data["grid_power"]

    @property
    def load_power(self) -> int:
        """Return load power in Watts."""
        # Add check to see if site has power metering?
        return self._power_data["load_power"]

    @property
    def solar_power(self) -> int:
        """Return solar power in Watts."""
        return self._power_data["solar_power"]

    @property
    def solar_type(self) -> int:
        """Return type of solar (e.g. pv_panels or roof)."""
        return self._energy_site["components"]["solar_type"]


class PowerwallSite(EnergySite):
    """Represents a Tesla Energy Powerwall site.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energy_site_objects`.
    """

    def __init__(self, api, energysite, power_data) -> None:
        """Initialize PowerwallSite."""
        super().__init__(api, energysite, power_data)
        # self.__default_real_mode = None
        # self.__backup_reserve_percent = None

    @property
    def battery_percent(self) -> int:
        """Return battery charge level percentage."""
        # Add check to see if site has power metering?
        return self._power_data["battery_percentage"]

    @property
    def battery_power(self) -> int:
        """Return battery power in Watts."""
        return self._power_data["battery_power"]

    @property
    def grid_power(self) -> int:
        # Grid and load power are the same in SolarSite because of how we store
        # the data. It comes from two different endpoints but we stored in self.__power_data
        return self._power_data["grid_power"]

    @property
    def load_power(self) -> int:
        """Return load power in Watts."""
        return self._power_data["load_power"]

    # async def set_operation_mode(self, real_mode, backup_reserve_percent) -> None:
    #     """Set operation mode of Powerwall."""
    #     # real_mode - self_consumption, backup, autonomous
    #     # backup_reserve_percent - 1-100
    #     data = await self._api(
    #         "BATTERY_OPERATION_MODE",
    #         path_vars={"battery_id": self.id},
    #         default_real_mode=real_mode,
    #         backup_reserve_percent=int(backup_reserve_percent),
    #     )
    #     if data and data["response"]["result"]:
    #         self.__default_real_mode = real_mode
    #         self.__backup_reserve_percent = backup_reserve_percent


class SolarPowerwallSite(PowerwallSite, SolarSite):
    """Represents a Tesla Energy Solar site with Powerwall(s).

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_energy_site_objects`.
    """

    def __init__(self, api, energysite, power_data) -> None:
        """Initialize SolarPowerwallSite."""
        super().__init__(api, energysite, power_data)
