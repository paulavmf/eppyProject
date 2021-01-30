from helpers import *
from shutil import copyfile
# SIMPLE ROOM CONSTANT AIR CONDITIONER FROM OPEN STUDIO LIBRARY, NO PEOPLE
# FROM OSM FILE: simple_room_1_window_1_door_ventilator_constant.osm

def main():
    idffile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/simple_room_1_window_1_door_unitary_System_sch_constant.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    # TODO buscar un fichero de temperatura coninental para este proyecto
    epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/Wheather file/FRA_Paris.Orly.071490_IWEC.epw'

    idf = initialization(idffile,iddfile,epwfile)

    objs_to_delete = ['PEOPLE','ELECTRICEQUIPMENT']
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    vars_name = ['Site Outdoor Air Drybulb Temperature','Zone Air Temperature']
    # TODO hacer esto general
    for n in range(len(vars_name)):
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][n].Variable_Name = vars_name[n]
    newdir = os.path.basename(__file__).replace('.py','')
    try:
        os.mkdir(newdir)
    except FileExistsError:
        print("Directory already exists")
    abs_newdir = os.path.join(os.getcwd(), newdir)
    idf.run(output_directory=os.path.join(os.getcwd(),newdir))
    # TODO esto no funciona, coge el directorio entero o desde el proyecto???
    copyfile(os.getcwd() + '/ReadVarsESO', abs_newdir+'/ReadVarsESO')
    # TODO está mal también que hacer el cambio y dar permisos...
    os.system(abs_newdir+'/ReadVarsESO')


if __name__ == '__main__':
    main()