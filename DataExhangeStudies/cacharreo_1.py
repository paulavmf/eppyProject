import sys
sys.path.insert(0, '/usr/local/EnergyPlus-9-4-0')
from pyenergyplus.api import EnergyPlusAPI

one_time = True
outdoor_temp_sensor = 0
outdoor_dew_point_sensor = 0
outdoor_dew_point_actuator = 0

idffile = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/input/simple_room_1_window_1_door_w_sensors.idf'
iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/input/wheather_file/FRA_Paris.Orly.071490_IWEC.epw'
output = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/APItesting/'

def time_step_handler(state):
    global one_time, outdoor_temp_sensor, outdoor_actuator
    sys.stdout.flush()
    if one_time:
        if api.exchange.api_data_fully_ready(state):
            # val = api.exchange.list_available_api_data_csv()
            # with open('/tmp/data.csv', 'w') as f:
            #     f.write(val.decode(encoding='utf-8'))
            outdoor_temp_sensor = api.exchange.get_variable_handle(
                state, u"People Radiant Heating Energy", u"ZONE"
            )
            outdoor_actuator = api.exchange.get_actuator_handle(
                state, "People", "Number of People", "THERMAL ZONE 1 189.1-2009 - OFFICE - OPENOFFICE - CZ4-8 PEOPLET"
            )
            if outdoor_temp_sensor == -1 or outdoor_actuator == -1:
                sys.exit(1)  # si alguna temperatura me da menos 1 sácame error...... ?¿?¿?¿?¿?¿ ehy???
            one_time = False

    day = api.exchange.day_of_month(state)
    month = api.exchange.month(state)
    min = api.exchange.minutes(state)

    if api.exchange.zone_time_step_number(state) == 1:
        hour = api.exchange.hour(state)
        # after_oa_temp = api.exchange.today_(state,3, 2)
        # print(f"Reading one hour later outdoor temp BEFORE actuation: {after_oa_temp}")
        print("actuator is seted")
        api.exchange.set_actuator_value(state, outdoor_actuator, 100)
        # after_oa_temp = api.exchange.today_weather_outdoor_dry_bulb_at_time(state, 3, 2)
        # print(f"Reading one hour later outdoor temp AFTER actuation: {after_oa_temp}")
        oa_temp = api.exchange.get_variable_value(state, outdoor_temp_sensor)
        print(f"Reading actuated outdoor temp via getVariable AFTER actuation, value is: {oa_temp} at {month}/{day} {hour}:{min}")
    if api.exchange.zone_time_step_number(state) == 3:
        hour = api.exchange.hour(state)
        # after_oa_temp = api.exchange.today_(state,3, 2)
        # print(f"Reading one hour later outdoor temp BEFORE actuation: {after_oa_temp}")
        print("actuator is seted")
        api.exchange.set_actuator_value(state, outdoor_actuator, 100)
        # after_oa_temp = api.exchange.today_weather_outdoor_dry_bulb_at_time(state, 3, 2)
        # print(f"Reading one hour later outdoor temp AFTER actuation: {after_oa_temp}")
        oa_temp = api.exchange.get_variable_value(state, outdoor_temp_sensor)
        print(f"Reading actuated outdoor temp via getVariable AFTER actuation, value is: {oa_temp} at {month}/{day} {hour}:{min}")

if __name__ == '__main__':
    api = EnergyPlusAPI()
    state = api.state_manager.new_state()
    api.runtime.callback_end_zone_timestep_after_zone_reporting(state, time_step_handler)
    api.exchange.request_variable(state, "People Radiant Heating Energy", "ZONE")
    # api.exchange.request_variable(state, "SITE OUTDOOR AIR DEWPOINT TEMPERATURE", "ENVIRONMENT")
    # trim off this python script name when calling the run_energyplus function so you end up with just
    # the E+ args, like: -d /output/dir -D /path/to/input.idf
    api.runtime.run_energyplus(state, ['-w', epwfile, idffile])