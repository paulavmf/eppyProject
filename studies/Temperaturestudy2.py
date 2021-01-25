from helpers import *
from shutil import copyfile
# SIMPLE ROOM CONSTANT AIR CONDITIONER FROM OPEN STUDIO LIBRARY, NO PEOPLE
# FROM OSM FILE: simple_room_1_window_1_door_ventilator_constant.osm

def main():
    idffile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/simple_room_1_window_1_door_ventilator_constant.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    # TODO buscar un fichero de temperatura coninental para este proyecto
    epwfile = '/usr/local/EnergyPlus-9-4-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw'

    idf = initialization(idffile,iddfile,epwfile)

    objs_to_delete = ['PEOPLE','ELECTRICEQUIPMENT']
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    vars_name = ['Site Outdoor Air Drybulb Temperature','Zone Air Temperature']
    # TODO hacer esto general
    idf.removeidfobject(idf.idfobjects['OUTPUT:VARIABLE'][0])
    for n in range(len(vars_name)):
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][n].Variable_Name = vars_name[n]
    newdir = os.path.basename(__file__).replace('.py','')
    try:
        os.mkdir(newdir)
    except FileExistsError:
        print("Directory already exists")
    idf.run(output_directory=os.path.join(os.getcwd(),newdir))
    # TODO esto no funciona, coge el directorio entero o desde el proyecto???
    copyfile('ReadVarsESO', newdir)
    os.system('/'.join(newdir,'ReadVarESO'))


if __name__ == '__main__':
    main()