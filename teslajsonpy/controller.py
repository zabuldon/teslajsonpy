import time
from multiprocessing import RLock
from teslajsonpy.connection import Connection
from teslajsonpy.BatterySensor import Battery, Range
from teslajsonpy.Lock import Lock, ChargerLock
from teslajsonpy.Climate import Climate, TempSensor
from teslajsonpy.BinarySensor import ParkingSensor, ChargerConnectionSensor
from teslajsonpy.Charger import ChargerSwitch, RangeSwitch
from teslajsonpy.GPS import GPS, Odometer
from teslajsonpy.Exceptions import TeslaException
from functools import wraps
from .Exceptions import RetryLimitError
import logging
_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, email, password, update_interval):
        self.__connection = Connection(email, password)
        self.__vehicles = []
        self.update_interval = update_interval
        self.__update = {}
        self.__climate = {}
        self.__charging = {}
        self.__state = {}
        self.__driving = {}
        self.__gui = {}
        self._last_update_time = {}
        self._last_wake_up_time = {}
        self.__lock = RLock()
        self._car_online = {}

        cars = self.get_vehicles()

        for car in cars:
            self._last_update_time[car['id']] = 0
            self._last_wake_up_time[car['id']] = 0
            self.__update[car['id']] = True
            self._car_online[car['id']] = car['state']
            self.__climate[car['id']] = False
            self.__charging[car['id']] = False
            self.__state[car['id']] = False
            self.__driving[car['id']] = False
            self.__gui[car['id']] = False

            try:
                self.update(car['id'], wake_if_asleep=False)
            except (TeslaException, RetryLimitError):
                pass
            self.__vehicles.append(Climate(car, self))
            self.__vehicles.append(Battery(car, self))
            self.__vehicles.append(Range(car, self))
            self.__vehicles.append(TempSensor(car, self))
            self.__vehicles.append(Lock(car, self))
            self.__vehicles.append(ChargerLock(car, self))
            self.__vehicles.append(ChargerConnectionSensor(car, self))
            self.__vehicles.append(ChargerSwitch(car, self))
            self.__vehicles.append(RangeSwitch(car, self))
            self.__vehicles.append(ParkingSensor(car, self))
            self.__vehicles.append(GPS(car, self))
            self.__vehicles.append(Odometer(car, self))

    def wake_up(f):
        """Wraps a API f so it will attempt to wake the vehicle if asleep.

        The command f is run once if the vehicle_id was last reported
        online. Assuming f returns None and wake_if_asleep is True, 5 attempts
        will be made to wake the vehicle to reissue the command.
        Args:
        inst (Controller): The instance of a controller
        vehicle_id (string): The vehicle to attempt to wake.
        wake_if_asleep (bool): Keyword arg to force a vehicle awake. Must be
                               set in the wrapped function f
        Throws:
        RetryLimitError
        """
        @wraps(f)
        def wrapped(*args, **kwargs):
            retries = 0
            sleep_delay = 2
            inst = args[0]
            vehicle_id = args[1]
            result = None
            if (vehicle_id is not None and vehicle_id in inst._car_online and
                    inst._car_online[vehicle_id]):
                try:
                    result = f(*args, **kwargs)
                except (TeslaException):
                    pass
            if result is not None:
                return result
            else:
                _LOGGER.debug("Wrapper: f:%s, result:%s, args:%s, kwargs:%s, "
                              "inst:%s, vehicle_id:%s, _car_online:%s" %
                              (f, result, args, kwargs, inst, vehicle_id,
                               inst._car_online))
                while ('wake_if_asleep' in kwargs and kwargs['wake_if_asleep']
                        and
                       (vehicle_id is None or
                        (vehicle_id is not None and
                         vehicle_id in inst._car_online and
                         not inst._car_online[vehicle_id]))):
                    result = inst._wake_up(vehicle_id, *args, **kwargs)
                    _LOGGER.debug("Result(%s): %s" % (retries, result))
                    if not result:
                        if retries < 5:
                            time.sleep(sleep_delay**(retries+2))
                            retries += 1
                            continue
                        else:
                            raise RetryLimitError
                    else:
                        break
                return f(*args, **kwargs)
        return wrapped

    def get_vehicles(self):
        return self.__connection.get('vehicles')['response']

    def post(self, vehicle_id, command, data={}):
        return self.__connection.post('vehicles/%i/%s' %
                                      (vehicle_id, command), data)

    def get(self, vehicle_id, command):
        return self.__connection.get('vehicles/%i/%s' % (vehicle_id, command))

    @wake_up
    def data_request(self, vehicle_id, name, wake_if_asleep=False):
        return self.get(vehicle_id, 'data_request/%s' % name)['response']

    @wake_up
    def command(self, vehicle_id, name, data={}, wake_if_asleep=True):
        return self.post(vehicle_id, 'command/%s' % name, data)

    def list_vehicles(self):
        return self.__vehicles

    def _wake_up(self, vehicle_id, *args, **kwargs):
        cur_time = int(time.time())
        if (not self._car_online[vehicle_id] or
                (cur_time - self._last_wake_up_time[vehicle_id] > 300)):
            result = self.post(vehicle_id, 'wake_up')['response']['state']
            _LOGGER.debug("Wakeup %s: %s" % (vehicle_id, result))
            self._car_online[vehicle_id] = result == 'online'
            self._last_wake_up_time[vehicle_id] = cur_time
        return self._car_online[vehicle_id]

    @wake_up
    def update(self, car_id, wake_if_asleep=False):
        cur_time = time.time()
        with self.__lock:
            # Check if any vehicles have been updated recently
            last_update = max(self._last_update_time.values())
            if (cur_time - last_update > self.update_interval):
                cars = self.get_vehicles()
                for car in cars:
                    self._car_online[car['id']] = car['state']
            # Only update online vehicles
            if (self._car_online[car_id] and
                    ((cur_time - self._last_update_time[car_id]) >
                        self.update_interval)):
                # Only update cars with update flag on
                data = (None if (car_id in self.__update and
                                 not self.__update[car_id]) else
                        self.get(car_id, 'data'))
                if data and data['response']:
                    self.__climate[car_id] = data['response']['climate_state']
                    self.__charging[car_id] = data['response']['charge_state']
                    self.__state[car_id] = data['response']['vehicle_state']
                    self.__driving[car_id] = data['response']['drive_state']
                    self.__gui[car_id] = data['response']['gui_settings']
                    self._car_online[car_id] = (data['response']['state']
                                                == 'online')
                self._last_update_time[car_id] = time.time()

    def get_climate_params(self, car_id):
        return self.__climate[car_id]

    def get_charging_params(self, car_id):
        return self.__charging[car_id]

    def get_state_params(self, car_id):
        return self.__state[car_id]

    def get_drive_params(self, car_id):
        return self.__driving[car_id]

    def get_gui_params(self, car_id):
        return self.__gui[car_id]

    def get_updates(self, car_id=None):
        if car_id is not None:
            return self.__update[car_id]
        else:
            return self.__update

    def set_updates(self, car_id, value):
        self.__update[car_id] = value
