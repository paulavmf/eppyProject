from helpers import *
from eppy.modeleditor import IDF
from eppy import idf_helpers
from eppy.bunch_subclass import EpBunch
import pandas as pd
import os
import random

def main():
    idffile = '/usr/local/EnergyPlus-9-4-0/ExampleFiles/1ZoneUncontrolled_win_1.idf'
    # iddfile = 'input/demo_simple.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    epwfile = '/usr/local/EnergyPlus-9-4-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw'
    file = '/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/output/1ZoneUncontrolled_win_1_out'
    idf = initialization(idffile, iddfile, epwfile)
    # arreglar el tema del datafile


    object_name = 'Site:GroundTemperature:BuildingSurface'
    instance = idf.idfobjects[object_name][0]
    outputfolder = 'output/simple/'

    for s in range(5):
        for field in instance.objls:
            if field != 'key' and field != 'Name':
                temperature =random.uniform(17,20)
                fieldsetter(instance,field,temperature)
        fieldsetter(idf.idfobjects['CONSTRUCTION:WINDOWDATAFILE'][0], 'File_Name',
                '/usr/local/EnergyPlus-9-4-0/DataSets/Window5DataFile.dat')
        variableName = 'ZONE ONE:Zone Windows Total Transmitted Solar Radiation Rate'
        idf.run(output_directory = file)
        if 'output' not in locals():
            output = get_outputs(file, variableName,str(s))
        else:
            tmp = get_outputs(file,variableName,str(s))
            output = pd.concat([output, tmp], axis=1)
    output.to_excel(file + '/output.xlsx')


if __name__ == '__main__':
    main()




