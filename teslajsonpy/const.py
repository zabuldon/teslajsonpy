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
WEBSOCKET_TIMEOUT = 11  # time for websocket to timeout
RELEASE_NOTES_URL = "https://teslascope.com/teslapedia/software/"
