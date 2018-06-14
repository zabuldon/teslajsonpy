from teslajsonpy.vehicle import VehicleDevice
import time


class FrontTrunk(VehicleDevice):
    def __init__(self, data, controller):
        super().__init__(data, controller)
        self.__manual_update_time = 0
        self.__front_trunk_state = False
        self.type = 'front trunk switch'
        self.hass_type = 'switch'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0xC
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_vehicle_params(self._id)
        if data and (time.time() - self.__manual_update_time > 60):
            self.__front_trunk_state = data['ft']

    def open_front_trunk(self):
        if not self.__front_trunk_state:
            data = self._controller.command(self._id, 'trunk_open', {"which_trunk": 'front'})
            if data and data['response']['result']:
                self.__front_trunk_state = True
            self.__manual_update_time = time.time()

    def is_open(self):
        return self.__front_trunk_state

    @staticmethod
    def has_battery():
        return False

class RearTrunk(VehicleDevice):
    def __init__(self, data, controller):
        super().__init__(data, controller)
        self.__manual_update_time = 0
        self.__rear_trunk_state = False
        self.type = 'rear trunk switch'
        self.hass_type = 'switch'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0xD
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_vehicle_params(self._id)
        if data and (time.time() - self.__manual_update_time > 60):
            self.__rear_trunk_state = data['rt']

    def open_rear_trunk(self):
        if not self.__rear_trunk_state:
            data = self._controller.command(self._id, 'trunk_open', {"which_trunk": 'rear'})
            if data and data['response']['result']:
                self.__rear_trunk_state = True
            self.__manual_update_time = time.time()

    def is_open(self):
        return self.__rear_trunk_state

    @staticmethod
    def has_battery():
        return False