import subprocess

from helpers.idf_helpers import *
from shutil import copyfile

def run_study(idf, objs_to_delete, vars_name, scriptname,filename = os.getcwd()):
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    # TODO hacer esto general
    for n in range(len(vars_name)):
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][n].Variable_Name = vars_name[n]
    # if idf.idfobjects['HVACTemplate:Thermostat']:
    #     schedule_name = idf.idfobjects['HVACTemplate:Thermostat'][0].Heating_Setpoint_Schedule_Name
    #     idf.newidfobject('OUTPUT:VARIABLE')
    #     idf.idfobjects['OUTPUT:VARIABLE'][-1].Key_Value = schedule_name
    #     idf.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Schedule Value'

    # newdir = os.path.basename(__file__).replace('.py','')
    foldername = scriptname.replace('.py', '')

    try:
        os.mkdir(foldername)
    except FileExistsError:
        print("Directory already exists")
    abs_newdir = os.path.join(os.path.dirname(__file__), foldername)
    idf.saveas(abs_newdir + '/idffile.idf')
    idf.run(output_directory=abs_newdir)
    copyfile(os.path.dirname(__file__) + '/ReadVarsESO', abs_newdir+'/ReadVarsESO')
    #TODO el misterio de permisos... no se...
    os.system(abs_newdir+'/ReadVarsESO')
    subprocess.run(abs_newdir+'/ReadVarsESO', shell=True, check=True)