# Developers Reference

## Core

The files that directly interact with the Tesla API are:
- [connection.py](teslajsonpy/connection.py) - low level access
- [controller.py](teslajsonpy/controller.py) - high level access and api

The controller provides a managed connection to a logged in session and will control access to all vehicles. It also performs throttling on certain commands to avoid overloading the Tesla API and will return cached copies of the JSON datastructure through the following commands.

- get_climate_params
- get_charging_params
- get_state_params
- get_config_params
- get_drive_params
- get_gui_params

If you want access to the API for your own app, you will likely only need to access these files.  The other files are examples of an implementation.

## Home Assistant
If you're looking to add functionality to Home Assistant you will need to do the following:
1. Check the [controller](teslajsonpy/controller.py) file to see if an appropriate API call exists. If necessary add them. Check out these references:
    - https://www.teslaapi.io/
    - https://tesla-api.timdorr.com/
2. Build a proper abstraction inheriting from the [vehicle.py](teslajsonpy/vehicle.py).  Check out [lock.py](teslajsonpy/lock.py).
3. Add abstraction to the controller [_add_components](https://github.com/zabuldon/teslajsonpy/blob/dev/teslajsonpy/controller.py#L530) so it will be discoverable.
3. Add changes to Home Assistant to access your abstraction and submit a PR per HA guidelines.
