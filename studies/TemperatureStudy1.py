from helpers.idf_helpers import *
from studies import run_study
# SIMPLE ROOM NO AIR CONDITIONER, NO PEOPLE, NO ELECTRICEQUIPMENT
def main():
    idffile = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/input/simple_room_1_window_1_door.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/EPProject/input/Wheather file/FRA_Paris.Orly.071490_IWEC.epw'

    idf = initialization(idffile,iddfile,epwfile)
    objs_to_delete = ['PEOPLE', 'LIGHTS', 'ELECTRICEQUIPMENT']
    vars_name = ['Site Outdoor Air Drybulb Temperature', 'Zone Air Temperature']

    run_study(idf, objs_to_delete, vars_name, scriptname=os.path.basename(__file__))






if __name__ == '__main__':
    main()



