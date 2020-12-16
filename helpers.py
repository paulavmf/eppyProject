from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import idf_helpers
import re
import pandas as pd
import os

def idfobjbypattern(idf,pattern):
    '''
    return a list of objects named according to a pattern
    '''
    objlst = []
    pattern = re.compile(pattern)
    for i in idf.idfobjects:
        if pattern.search(i):
            objlst.append(i)
    return objlst

def fieldsetter(epbunch,fieldname, newvalue):
    epbunch.__setattr__(fieldname, newvalue)


def get_instance(idf, ObjectName, NameToStudy):
    '''

    '''
    object_schedule = ObjectName
    schedule_instance = list(filter(lambda x: x.Name == NameToStudy, idf.idfobjects[object_schedule]))[0]
    return schedule_instance

def initialization(idffile, iddfile,epwfile):
    IDF.setiddname(iddfile)
    idf = IDF(idffile, epwfile)
    return idf

def get_outputs(fname, variableName = None, scheduleName = None):
    # TODO hacerlo para una lista de variables
    '''
    Create a dataframe from eplusout.eso with the output variable to study
    '''
    os.startfile(fname+"/ReadVarsESO.exe")
    data = pd.read_csv(fname+'/eplusout.csv')
    data = data.set_index('Date/Time')
    if variableName:
        pattern = re.compile(variableName)
        for i in data.columns:
            if pattern.search(i): # me dará como resultado todas las thermas zones..
                col = i
        data = data[col].to_frame()
        data.rename(columns = {col : ':'.join([col, scheduleName])}, inplace = True)
    return data

def epobject_to_df(epobj):
    # todo revisar que funciona para todos los objetos
    'Convert an ep object in a pandas dataframe for a netter visualization'
    df = pd.DataFrame({'fields': epobj[0].fieldnames})
    col = 0
    for o in epobj:
        col =col +1
        df[str(col)] = o.obj
    df = df.set_index('fields')
    return df

def notnullobj(idf):
    l = []
    # TODO no funciona en ypynb
    for i in idf.idfobjects:
        if len(idf.idfobjects[i])>0:
            l.append(i)
    return l
