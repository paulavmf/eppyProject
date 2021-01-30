import sys

from pandas.core.reshape.merge import merge
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)
from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import idf_helpers
from eppy.bunch_subclass import EpBunch
import pandas as pd
import os
from helpers.idf_helpers import fieldsetter, initialization
import re

# TODO HACER UN PROGRAMA GENÉRICO PARA CAMBIAR LO SCHEDULES DE ALGO ESPECÍFICO...



def get_outputs(variableName, scheduleName):
    # TODO hacerlo para una lista de variables
    '''
    Create a dataframe from eplusout.eso with the output variable to study
    '''
    os.system('/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/output/schedule/ReadVarsESO')
    data = pd.read_csv('/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/output/schedule/eplusout.csv')
    data = data.set_index('Date/Time')
    pattern = re.compile(variableName)
    for i in data.columns:
        if pattern.search(i): # me dará como resultado todas las thermas zones..
            col = i
    data = data[col].to_frame()
    data.rename(columns = {col : ':'.join([col, scheduleName])}, inplace = True)
    return data

def plotSimulation(df):
    pass


def get_schedule_instance(idf, scheduleObjectName, instanceNameToStudy):
    '''

    '''
    object_schedule = scheduleObjectName
    schedule_instance = list(filter(lambda x: x.Name == instanceNameToStudy, idf.idfobjects[object_schedule]))[0]
    return schedule_instance

# después de esto tengo que bajar al nivel de schedule day.

def main():
    idffile = 'input/demo_simple.idf'
    iddfile = '/usr/local/EnergyPlus-9-4-0/Energy+.idd'
    epwfile = '/usr/local/EnergyPlus-9-4-0/WeatherData/USA_CO_Golden-NREL.724666_TMY3.epw'
    idf = initialization(idffile, iddfile,epwfile)
    # Schedule Ro Change Office Activity
    object_schedule = 'Schedule:Year'
    # look for the object on Schedule:Year Objects with Name is Office Activity
    # TODO office activity qué es en realidad?
    scheduleYear_instance = list(filter(lambda x: x.Name == 'Office Activity',idf.idfobjects[object_schedule]))[0]
    # Name of the Schedule:Week Instance 
    scheduleWeek_Name = scheduleYear_instance.ScheduleWeek_Name_1
    # schedule:week:daily object contiene los schedules diarios para cada día de la semana y días de fiesta
    # hago un filtrado del que atiende al schedule Year usado para Office Activity
    # Este es el objeto a modificar
    scheduleWeekDaily_instance = list(filter(lambda x: x.Name == scheduleWeek_Name, idf.idfobjects['Schedule:Week:Daily']))[0]
    # lista de Schedules que voy a usar
    scheduleDayInterval_list =  [obj.Name for obj in idf.idfobjects['SCHEDULE:DAY:INTERVAL']][:2]
    # remove all outputs TENGO QUE USAR LA FUNCIÓN FILTER:
    fieldsetter(idf.idfobjects['SIMULATIONCONTROL'][0], 'Run_Simulation_for_Sizing_Periods', 'No')
    fieldsetter(idf.idfobjects['SIMULATIONCONTROL'][0], 'Run_Simulation_for_Weather_File_Run_Periods', 'Yes')

    for var in idf.idfobjects['Output:Variable']:
        if var.Variable_Name != 'People Radiant Heating Rate':
            idf.removeidfobject(var)
    # rename fields of interest TENGO QUE USAR LA FUNCIÓN FILTER
    for sch in scheduleDayInterval_list:
        for field in scheduleWeekDaily_instance.objls:
            if field != 'key' and field !='Name':
                fieldsetter(scheduleWeekDaily_instance,field, sch)
        idf.run(output_directory = 'output/schedule/')
        if not 'output' in locals():
            output = get_outputs('People Radiant Heating Rate', sch)
        else:
            tmp = get_outputs('People Radiant Heating Rate',sch)
            output = pd.concat([output, tmp ], axis = 1)
    output.to_excel('output/output.xlsx')

if __name__ == "__main__":
    main()

