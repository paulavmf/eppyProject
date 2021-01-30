from helpers import *
# SIMPLE ROOM with people and no AIR CONDITIONER,

def main():
    idffile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/simple_room_1_window_1_door.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    # TODO buscar un fichero de temperatura coninental para este proyecto
    epwfile = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/input/Wheather file/FRA_Paris.Orly.071490_IWEC.epw'

    idf = initialization(idffile,iddfile,epwfile)

    objs_to_delete = ['LIGHTS', 'ELECTRICEQUIPMENT']
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    vars_name = ['Site Outdoor Air Drybulb Temperature', 'Zone Air Temperature']
    # TODO hacer esto general
    if len(idf.idfobjects['OUTPUT:VARIABLE'])>0:
        for o in idf.idfobjects['OUTPUT:VARIABLE']:
            idf.removeidfobject(o)
    for n in range(len(vars_name)):
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][n].Variable_Name = vars_name[n]
    newdir = os.path.basename(__file__).replace('.py', '')
    try:
        os.mkdir(newdir)
    except FileExistsError:
        print("Directory already exists")
    abs_newdir = os.path.join(os.getcwd(), newdir)
    idf.run(output_directory=abs_newdir)
    # TODO dice que el archivo no existe' muy raro
    #os.system('output/no_HVC_no_people_study/ReadVarsESO')



if __name__ == '__main__':
    main()