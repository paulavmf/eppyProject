from helpers import *
from shutil import copyfile

def run_TemperatureStudy(idf, objs_to_delete, vars_name, scriptname):
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    # vars_name = ['Site Outdoor Air Drybulb Temperature','Zone Air Temperature']
    # TODO hacer esto general
    for n in range(len(vars_name)):
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][n].Variable_Name = vars_name[n]
    # newdir = os.path.basename(__file__).replace('.py','')
    newdir = scriptname.replace('.py', '')

    try:
        os.mkdir(newdir)
    except FileExistsError:
        print("Directory already exists")
    abs_newdir = os.path.join(os.getcwd(), newdir)
    idf.saveas(abs_newdir + 'idffile.idf')
    idf.run(output_directory=abs_newdir)
    # TODO esto no funciona, coge el directorio entero o desde el proyecto???
    copyfile(os.getcwd() + '/ReadVarsESO', abs_newdir+'/ReadVarsESO')
    # TODO está mal también que hacer el cambio y dar permisos...
    os.system(abs_newdir+'/ReadVarsESO')