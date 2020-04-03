#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle state model."""

from typing import Text


class MediaStateModel:  # pylint: disable-msg=R0903
    """Tesla vehicle media state model.

    The model is represented by the vehicle state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/vehiclestate
    """

    def __init__(self):
        """Initialize the media state model."""

        self.__remote_control_enabled = None

    @property
    def remote_control_enabled(self) -> bool:
        """Return the remote_control_enabled."""
        return self.__remote_control_enabled


class SoftwareUpdateModel:
    """Tesla vehicle software update model.

    The model is represented by the vehicle state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/vehiclestate
    """

    def __init__(self):
        """Initialize the software update model."""

        self.__download_perc = None
        self.__expected_duration_sec = None
        self.__install_perc = None
        self.__scheduled_time_ms = None
        self.__status = None
        self.__version = None

    @property
    def download_perc(self) -> int:
        """Return the download_perc."""
        return self.__download_perc

    @property
    def expected_duration_sec(self) -> int:
        """Return the expected_duration_sec."""
        return self.__expected_duration_sec

    @property
    def install_perc(self) -> int:
        """Return the install_perc."""
        return self.__install_perc

    @property
    def scheduled_time_ms(self) -> int:
        """Return the scheduled_time_ms."""
        return self.__scheduled_time_ms

    @property
    def status(self) -> Text:
        """Return the status."""
        return self.__status

    @property
    def version(self) -> Text:
        """Return the version."""
        return self.__version


class SpeedLimitModeModel:
    """Tesla vehicle speed limit mode model.

    The model is represented by the vehicle state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/vehiclestate
    """

    def __init__(self):
        """Initialize the speed limit mode model."""

        self.__active = None
        self.__current_limit_mph = None
        self.__max_limit_mph = None
        self.__min_limit_mph = None
        self.__pin_code_set = None

    @property
    def active(self) -> bool:
        """Return the active."""
        return self.__active

    @property
    def current_limit_mph(self) -> bool:
        """Return the current_limit_mph."""
        return self.__current_limit_mph

    @property
    def max_limit_mph(self) -> bool:
        """Return the max_limit_mph."""
        return self.__max_limit_mph

    @property
    def min_limit_mph(self) -> bool:
        """Return the min_limit_mph."""
        return self.__min_limit_mph

    @property
    def pin_code_set(self) -> bool:
        """Return the pin_code_set."""
        return self.__pin_code_set


class VehicleStateModel:  # pylint: disable-msg=R0904
    """Tesla vehicle state model.

    The model is represented by the vehicle state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/vehiclestate
    """

    def __init__(self):
        """Initialize the vehicle state model."""

        self.__api_version = None
        self.__autopark_state_v3 = None
        self.__autopark_style = None
        self.__calendar_supported = None
        self.__car_version = None
        self.__center_display_state = None
        self.__df = None
        self.__dr = None
        self.__fd_window = None
        self.__fp_window = None
        self.__ft = None
        self.__homelink_device_count = None
        self.__homelink_nearby = None
        self.__is_user_present = None
        self.__last_autopark_error = None
        self.__locked = None
        self.__media_state = None
        self.__notifications_supported = None
        self.__odometer = None
        self.__parsed_calendar_supported = None
        self.__pf = None
        self.__pr = None
        self.__rd_window = None
        self.__remote_start = None
        self.__remote_start_enabled = None
        self.__remote_start_supported = None
        self.__rp_window = None
        self.__rt = None
        self.__sentry_mode = None
        self.__sentry_mode_available = None
        self.__smart_summon_available = None
        self.__software_update = None
        self.__speed_limit_mode = None
        self.__summon_standby_mode_enabled = None
        self.__sun_roof_percent_open = None
        self.__sun_roof_state = None
        self.__timestamp = None
        self.__valet_mode = None
        self.__valet_pin_needed = None
        self.__vehicle_name = None

    @property
    def api_version(self) -> int:
        """Return the api_version."""
        return self.__api_version

    @property
    def autopark_state_v3(self) -> Text:
        """Return the autopark_state_v3."""
        return self.__autopark_state_v3

    @property
    def autopark_style(self) -> Text:
        """Return the autopark_style."""
        return self.__autopark_style

    @property
    def calendar_supported(self) -> bool:
        """Return the calendar_supported."""
        return self.__calendar_supported

    @property
    def car_version(self) -> Text:
        """Return the car_version."""
        return self.__car_version

    @property
    def center_display_state(self) -> int:
        """Return the center_display_state."""
        return self.__center_display_state

    @property
    # pylint: disable=C0103
    def df(self) -> int:
        """Return the df."""
        return self.__df

    @property
    # pylint: disable=C0103
    def dr(self) -> int:
        """Return the dr."""
        return self.__dr

    @property
    def fd_window(self) -> int:
        """Return the fd_window."""
        return self.__fd_window

    @property
    def fp_window(self) -> int:
        """Return the fp_window."""
        return self.__fp_window

    @property
    # pylint: disable=C0103
    def ft(self) -> int:
        """Return the ft."""
        return self.__ft

    @property
    def homelink_device_count(self) -> int:
        """Return the homelink_device_count."""
        return self.__homelink_device_count

    @property
    def homelink_nearby(self) -> bool:
        """Return the homelink_nearby."""
        return self.__homelink_nearby

    @property
    def is_user_present(self) -> bool:
        """Return the is_user_present."""
        return self.__is_user_present

    @property
    def last_autopark_error(self) -> Text:
        """Return the last_autopark_error."""
        return self.__last_autopark_error

    @property
    def locked(self) -> bool:
        """Return the locked."""
        return self.__locked

    @property
    def media_state(self) -> MediaStateModel:
        """Return the media_state."""
        return self.__media_state

    @property
    def notifications_supported(self) -> bool:
        """Return the notifications_supported."""
        return self.__notifications_supported

    @property
    def odometer(self) -> float:
        """Return the odometer."""
        return self.__odometer

    @property
    def parsed_calendar_supported(self) -> bool:
        """Return the parsed_calendar_supported."""
        return self.__parsed_calendar_supported

    @property
    # pylint: disable=C0103
    def pf(self) -> int:
        """Return the pf."""
        return self.__pf

    @property
    # pylint: disable=C0103
    def pr(self) -> int:
        """Return the pr."""
        return self.__pr

    @property
    def rd_window(self) -> int:
        """Return the rd_window."""
        return self.__rd_window

    @property
    def remote_start(self) -> bool:
        """Return the remote_start."""
        return self.__remote_start

    @property
    def remote_start_enabled(self) -> bool:
        """Return the remote_start_enabled."""
        return self.__remote_start_enabled

    @property
    def remote_start_supported(self) -> bool:
        """Return the remote_start_supported."""
        return self.__remote_start_supported

    @property
    def rp_window(self) -> int:
        """Return the rp_window."""
        return self.__rp_window

    @property
    # pylint: disable=C0103
    def rt(self) -> int:
        """Return the rt."""
        return self.__rt

    @property
    def sentry_mode(self) -> bool:
        """Return the sentry_mode."""
        return self.__sentry_mode

    @property
    def sentry_mode_available(self) -> bool:
        """Return the sentry_mode_available."""
        return self.__sentry_mode_available

    @property
    def smart_summon_available(self) -> bool:
        """Return the smart_summon_available."""
        return self.__smart_summon_available

    @property
    def software_update(self) -> SoftwareUpdateModel:
        """Return the software_update."""
        return self.__software_update

    @property
    def speed_limit_mode(self) -> SpeedLimitModeModel:
        """Return the speed_limit_mode."""
        return self.__speed_limit_mode

    @property
    def summon_standby_mode_enabled(self) -> bool:
        """Return the summon_standby_mode_enabled."""
        return self.__summon_standby_mode_enabled

    @property
    def sun_roof_percent_open(self) -> bool:
        """Return the sun_roof_percent_open."""
        return self.__sun_roof_percent_open

    @property
    def sun_roof_state(self) -> Text:
        """Return the sun_roof_state."""
        return self.__sun_roof_state

    @property
    def timestamp(self) -> int:
        """Return the timestamp."""
        return self.__timestamp

    @property
    def valet_mode(self) -> bool:
        """Return the valet_mode."""
        return self.__valet_mode

    @property
    def valet_pin_needed(self) -> bool:
        """Return the valet_pin_needed."""
        return self.__valet_pin_needed

    @property
    def vehicle_name(self) -> Text:
        """Return the vehicle_name."""
        return self.__vehicle_name
