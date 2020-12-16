from helpers import *
from eppy.modeleditor import IDF
from eppy import idf_helpers
from eppy.bunch_subclass import EpBunch
import pandas as pd
import os
import random

def main():
    iddfile = r'C:\EnergyPlusV9-4-0\Energy+.idd'
    idffile = r'C:\EnergyPlusV9-4-0\ExampleFiles\1ZoneUncontrolled_win_1.idf'
    epwfile = 'C:/EnergyPlusV9-4-0/WeatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw'
    idf = initialization(idffile, iddfile, epwfile)
    # arreglar el tema del datafile


    object_name = 'Site:GroundTemperature:BuildingSurface'
    instance = idf.idfobjects[object_name][0]
    simulationnumber = 5
    outputfolder = 'output/simple/'

    for field in instance.objls:
        if field != 'key' and field != 'Name':
            temperature =random.uniform(17,20)
            fieldsetter(instance,field,temperature)

    idf.run(output_directory = outputfolder)
    output = get_outputs(outputfolder)
    output.to_excel('output/output.xlsx')


if __name__ == '__main__':
    main()




