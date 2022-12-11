#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
IDLE_INTERVAL = 600  # interval after parking to check at regular update_interval
ONLINE_INTERVAL = 60  # interval for checking online state; does not hit individual cars
SLEEP_INTERVAL = 660  # interval required to let vehicle sleep; based on testing
DRIVING_INTERVAL = 60  # interval when driving detected
UPDATE_INTERVAL = 300  # Default polling interval for vehicle
WEBSOCKET_TIMEOUT = 11  # time for websocket to timeout
WAKE_TIMEOUT = 60  # max time to wait for vehicle to wake
WAKE_CHECK_INTERVAL = 2  # wait period between wake checks after a wake request
RELEASE_NOTES_URL = "https://teslascope.com/teslapedia/software/"
AUTH_DOMAIN = "https://auth.tesla.com"
API_URL = "https://owner-api.teslamotors.com"
WS_URL = "wss://streaming.vn.teslamotors.com/streaming"

TESLA_PRODUCT_TYPE_VEHICLES = "vehicles"

BACKUP_RESERVE_MAX = 100
BACKUP_RESERVE_MIN = 0
CHARGE_CURRENT_MIN = 0
DEFAULT_ENERGYSITE_NAME = "My Home"
GRID_ACTIVE = "Active"
PRODUCT_TYPE_ENERGY_SITES = "energy_sites"
PRODUCT_TYPE_POWERWALLS = "powerwalls"
RESOURCE_TYPE = "resource_type"
RESOURCE_TYPE_SOLAR = "solar"
RESOURCE_TYPE_BATTERY = "battery"

STATUS_ONLINE = "online"  # reported by Tesla, vehicle available and awake
STATUS_ASLEEP = "asleep"  # reported by Tesla, vehicle available but asleep
STATUS_OFFLINE = "offline"  # reported by Tesla, vehicle offline, wake/sleep unknown
STATUS_UNAVAILABLE = "unavailable"  # set by Controller after successive api failures, overrides the above
STATUS_UNKNOWN = "unknown"  # set by Controller during initialization, default value
