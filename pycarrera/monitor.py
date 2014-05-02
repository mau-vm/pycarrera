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
	            fuel_level = 'unknown'

                self.race_status_info[car_number]['fuel_level'] = fuel_level

            mystery_levels = response[7:8]

            race_state = int(chr(response[9]))
            
            if race_state == 0:
                self.race_status_info['race_state'] = 'running'
            elif race_state == 1:
                self.race_status_info['race_state'] = 'ready'
            elif race_state == 9:
                self.race_status_info['race_state'] = 'false_start'
	    else:
                self.race_status_info['race_state'] = start_count



            fuel_tank_mode = response[10]
	    
            if fuel_tank_mode == ord('0'):
                fuel_tank_mode = 'off'
            elif fuel_tank_mode == ord('1'):
                fuel_tank_mode = 'normal'
            elif fuel_tank_mode == ord('2'):
                fuel_tank_mode = 'real'
            else:
                fuel_tank_mode = 'unknown'


            self.race_status_info['fuel_tank_mode'] = fuel_tank_mode

            refuel_bitmask = response[11:12]

            self.race_status_info['position_tower_type'] = chr(response[13])

        else:
            car_number = int(chr(response[0]))
            last_crossed_tuple = struct.unpack_from('I', str(response[1:8]))
            last_crossed_timestamp = last_crossed_tuple[0]

            sensor_group = response[9]

            if not car_number in self.race_status_info:
                self.race_status_info[car_number] = {}

            car_info = self.race_status_info[car_number]

            if not 'splits' in car_info:
                car_info['splits'] = []

	    if not last_crossed_timestamp in car_info['splits']:
                if self.race_status_info[car_number]['splits']:
                    self.race_status_info[car_number]['last_laptime'] = last_crossed_timestamp - self.race_status_info[car_number]['splits'][-1] 
                self.race_status_info[car_number]['splits'].append(last_crossed_timestamp)

        return self.race_status_info
