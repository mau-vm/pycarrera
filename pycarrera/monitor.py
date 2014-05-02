import struct
from client import ControlUnitClient

LAP_IN_PROGRESS_INDICATOR = ':'
FUEL_TANK_MODE_OFF = 0
FUEL_TANK_MODE_NORMAL = 1
FUEL_TANK_MODE_REAL = 2

class CommunicationException(Exception):
    pass

class RaceMonitor(object):
    """."""
    def __init__(self, serial_port):
        self.client = ControlUnitClient(serial_port)
        self.race_status_info = {}

    @property
    def race_status(self):
        """This command returns two types of statuses:
        - A 'finish line' status, where the last car to cross the finish line's number and time is returned.
        - A 'lap in progress' status (preceded by a ':' character), which gives the fuel levels for each car."""
        response = self.client.race_status

        if chr(response[0]) == LAP_IN_PROGRESS_INDICATOR:
            for car_number in range(1, 7):
		if car_number not in self.race_status_info:
		    self.race_status_info[car_number] = {}

		fuel_level = response[car_number]

		if fuel_level == ord('?'):
	            fuel_level = 'UNKNOWN'

                self.race_status_info[car_number]['fuel_level'] = fuel_level

            mystery_levels = response[7:8]
            self.race_status_info['start_count'] = chr(response[9])

            fuel_tank_mode = chr(response[10])
            self.race_status_info['fuel_tank_mode'] = fuel_tank_mode

            refuel_bitmask = response[11:12]

            self.race_status_info['position_tower_type'] = chr(response[13])

        else:
            car_number = response[0]
            last_crossed_timestamp = response[1:8]
            sensor_group = response[9]

            if not car_number in self.race_status_info:
                self.race_status_info[car_number] = {}
                self.race_status_info[car_number]['splits'] = []

            race_info = self.race_status_info[car_number]

            if race_info['splits']:
                race_info['last_laptime_in_millis'] = last_crossed_timestamp - race_info['splits'][-1]

            self.race_status_info[car_number]['splits'].append(last_crossed_timestamp)

	print response
        return self.race_status_info
