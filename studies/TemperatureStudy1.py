from helpers import *
# SIMPLE ROOM NO AIR CONDITIONER, NO PEOPLE, NO ELECTRICEQUIPMENT

def main():
    idffile = 'input/simple_room_1_window_1_door_output_vars.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    # TODO buscar un fichero de temperatura coninental para este proyecto
    epwfile = '/usr/local/EnergyPlus-9-4-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw'

    idf = initialization(idffile,iddfile,epwfile)

    objs_to_delete = ['PEOPLE', 'LIGHTS', 'ELECTRICEQUIPMENT']
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    vars_name = ['Site Outdoor Air Drybulb Temperature','Zone Air Temperature']

    idf.run(output_directory = 'output/no_HVC_no_people_study')
    # TODO dice que el archivo no existe' muy raro
    os.system('/output/no_HVC_no_people_study/ReadVarsESO')


if __name__ == '__main__':
    main()



