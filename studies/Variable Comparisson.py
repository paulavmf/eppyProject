from helpers.idf_helpers import *
from studies import *


def main():
    idffile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/simple_room_1_window_1_door_unitary_System_sch_small_office_Activity.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/Wheather file/FRA_Paris.Orly.071490_IWEC.epw'

    idf = initialization(idffile,iddfile,epwfile)
    objs_to_delete = []
    vars_name = ['Site Outdoor Air Drybulb Temperature','Zone Mean Air Temperature', 'Zone Operative Temperature', 'Zone Air Temperature','Zone Air Temperature','Zone Thermostat Air Temperature']
    HVAC_Average = ['Zone Air Temperature','Zone Thermostat Air Temperature']

    run_study(idf, objs_to_delete, vars_name, os.path.basename(__file__))



if __name__ == '__main__':
    main()