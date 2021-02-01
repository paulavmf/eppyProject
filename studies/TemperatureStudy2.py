from helpers.idf_helpers import *
from studies import run_study
# SIMPLE ROOM CONSTANT AIR CONDITIONER FROM OPEN STUDIO LIBRARY, NO PEOPLE
# FROM OSM FILE: simple_room_1_window_1_door_ventilator_constant.osm
'''
__TemperatureStudy2__:

- PEOPLE: NO
- LIGHTS: NO
- ELECTRICEQUIPMENT: NO
- AIRCONDITIONER: SÍ
  - DATOS:
              key 	HVACTemplate:Thermostat
              Name 	thermostat 1
              Heating_Setpoint_Schedule_Name 	Always On Continuous
              Constant_Heating_Setpoint 	15
              Cooling_Setpoint_Schedule_Name 	
              Constant_Cooling_Setpoint 	25
              -----------------------------
              fields: 	
              key 	HVACTemplate:Thermostat
              Name 	thermostat 1
              Heating_Setpoint_Schedule_Name 	Always On Continuous
              Constant_Heating_Setpoint 	15
              Cooling_Setpoint_Schedule_Name 	
              Constant_Cooling_Setpoint 	25
              -------------------------------
              key 	HVACTemplate:Zone:Unitary
              Zone_Name 	Thermal Zone 1
              Template_Unitary_System_Name 	system 1
              Template_Thermostat_Name 	thermostat 1
              Supply_Air_Maximum_Flow_Rate 	autosize
'''


def main():
    idffile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/simple_room_1_window_1_door_unitary_System_sch_constant.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/Wheather file/FRA_Paris.Orly.071490_IWEC.epw'

    idf = initialization(idffile,iddfile,epwfile)
    objs_to_delete = ['PEOPLE','ELECTRICEQUIPMENT']
    vars_name = ['Site Outdoor Air Drybulb Temperature','Zone Air Temperature']

    run_study(idf, objs_to_delete, vars_name, os.path.basename(__file__))



if __name__ == '__main__':
    main()