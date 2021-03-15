import subprocess

from helpers.idf_helpers import *
from shutil import copyfile

vars_name = [
    'Zone Mean Radiant Temperature',
             'Zone Mean Air Temperature',
             'Zone Operative Temperature',
             'Zone Mean Air Dewpoint Temperature',
             'Zone Outdoor Air Wetbulb Temperature',
             'Zone Air Temperature',
             'Zone Thermostat Air Temperature',
             'Zone Thermostat Heating Setpoint Temperature',
             'Zone Thermostat Cooling Setpoint Temperature',
             'Zone Adaptive Comfort Operative Temperature Set Point',
             'Zone Heat Index']

def run_study(idf, objs_to_delete, vars_name, scriptname=None,new_folder_path = None, convert = False):
    for obj in objs_to_delete:
        for o in idf.idfobjects[obj]:
            idf.removeidfobject(o)
    for n in range(len(vars_name)):
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][n].Variable_Name = vars_name[n]
    if scriptname:
        foldername = scriptname.replace('.py', '')
        abs_newdir = os.path.join(os.path.dirname(__file__), foldername)
    elif new_folder_path:
        abs_newdir = new_folder_path
    else:
        abs_newdir = os.path.join(os.path.dirname(__file__))
    try:
        os.mkdir(abs_newdir)
    except FileExistsError:
        print("Directory already exists")

    idf.saveas(abs_newdir + '/idffile.idf')
    idf.run(output_directory=abs_newdir)
    if convert:
        copyfile(os.path.dirname(__file__) + '/ReadVarsESO', abs_newdir+'/ReadVarsESO')
        cmd = "cd"+ abs_newdir
        subprocess.run(["cd"+ abs_newdir])
        subprocess.run(["./ReadVarsESO"])
        #TODO el misterio de permisos... no se...