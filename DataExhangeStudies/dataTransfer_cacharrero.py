'''
from https://github.com/NREL/EnergyPlus/blob/develop/tst/EnergyPlus/api/TestDataTransfer.py
with some annotations just to try
'''

import sys

sys.path.insert(0, '/usr/local/EnergyPlus-9-4-0')
from pyenergyplus.api import EnergyPlusAPI

idffile = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/input/simple_room_1_window_1_door_w_sensors.idf'
iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/input/wheather_file/FRA_Paris.Orly.071490_IWEC.epw'
output = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/APItesting/'

one_time = True
outdoor_temp_sensor = 0
outdoor_dew_point_sensor = 0
outdoor_dew_point_actuator = 0

# First I have to add the sensors through Epi, for example
sensor = 'Site Outdoor Air Drybulb Temperature'
zone = 'Zone'


def time_step_handler(state):
    global one_time, ZoneTemp
    sys.stdout.flush()
    if one_time:
        if api.exchange.api_data_fully_ready(state):  #
            ZoneTemp = api.exchange.get_variable_handle(
                state, sensor, zone)
    dryTemp = api.exchange.get_variable_value(state, outdoor_dew_point_sensor)
    print("Reading outdoor temp via getVariable, value is: %s" % dryTemp)


if __name__ == '__main__':
    api = EnergyPlusAPI()
    state = api.state_manager.new_state()
    api.runtime.callback_end_zone_timestep_after_zone_reporting(state, time_step_handler)
    api.exchange.request_variable(state, sensor, zone)
    api.runtime.run_energyplus(state, ['-w', epwfile, idffile])