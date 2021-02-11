from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy import idf_helpers
import re
import pandas as pd
import os


def idfobjbypattern(idf, pattern, null=False):
    '''
    return a list of objects named according to a pattern
    '''
    objlst = []
    pattern = re.compile(pattern)
    if not null:
        idfobjs = notnullobj(idf)
    else:
        idfobjs = idf.idfobjects
    for i in idfobjs:
        if pattern.search(i):
            objlst.append(i)
    return objlst


def fieldsetter(epbunch, fieldname, newvalue):
    epbunch.__setattr__(fieldname, newvalue)


def fieldgetter(epbunch, fieldname):
    return epbunch.__getattr__(fieldname)


def get_schedule_instance(idf, instanceNameToStudy, scheduleObjectName=None):
    '''

    '''
    if not scheduleObjectName:
        sch_Obj_list = idfobjbypattern(idf, 'SCHEDULE')
        schedule_instance = []
        for object_schedule in sch_Obj_list:
            tmp = list(filter(lambda x: x.Name == instanceNameToStudy, idf.idfobjects[object_schedule]))
            if len(tmp)==1:
                schedule_instance.append(
                    tmp[0]
                )
            if len(tmp)>1:
                raise Exception('Same schedule found more than once in the same Obj')
        if len(schedule_instance) > 1:
            print('more than one schedule with the same name')
            return (schedule_instance)
        else:
            return (schedule_instance[0])
    else:
        object_schedule = scheduleObjectName
        schedule_instance = list(filter(lambda x: x.Name == instanceNameToStudy, idf.idfobjects[object_schedule]))[0]
        return schedule_instance


def get_instance(idf, ObjectName, NameToStudy):
    '''

    '''
    object_schedule = ObjectName
    schedule_instance = list(filter(lambda x: x.Name == NameToStudy, idf.idfobjects[object_schedule]))[0]
    return schedule_instance


def initialization(idffile, iddfile, epwfile):
    IDF.setiddname(iddfile)
    idf = IDF(idffile, epwfile)
    return idf


def get_outputs(fname, variableName=None, scheduleName=None):
    # TODO hacerlo para una lista de variables
    '''
    Create a dataframe from eplusout.eso with the output variable to study
    '''
    os.startfile(fname + "/ReadVarsESO.exe")
    data = pd.read_csv(fname + '/eplusout.csv')
    data = data.set_index('Date/Time')
    if variableName:
        pattern = re.compile(variableName)
        for i in data.columns:
            if pattern.search(i):  # me dará como resultado todas las thermas zones..
                col = i
        data = data[col].to_frame()
        data.rename(columns={col: ':'.join([col, scheduleName])}, inplace=True)
    return data


def epobject_to_df(epobj):
    'Convert an ep object in a pandas dataframe for a netter visualization'
    df = pd.DataFrame({'fields': epobj[0].objls})
    col = 0
    for o in epobj:
        col += 1
        df[str(col)] = [fieldgetter(o, f) for f in o.objls]
    df = df.set_index('fields')
    return df


def notnullobj(idf):
    l = []
    for i in idf.idfobjects:
        if len(idf.idfobjects[i]) > 0:
            l.append(i)
    return l


def eso_to_ts(outputfile, drop_duplicateds=False):
    df = pd.read_csv(outputfile)
    if drop_duplicateds:
        df = df.drop_duplicates()
        # TODO ENSEÑAR LOS DUPLICADOS O ALGO ASÍ O HACER ESTO CONTANDO LOS VALORES QUE DEBERÍA TENER
    if sum(df['Date/Time'].duplicated()) > 0:
        raise Exception('dates are duplicated. Impossible to convert to Time Series data frame')
    new = df['Date/Time'].str.split('  ', n=1, expand=True)
    new[0] = new[0].str.replace('/', '-') + '-00'
    new[1] = new[1].str.replace('24',
                                '00')  # TODO esto  tengo que hacerlo por regex si mis simulaciones son más cortas
    # que una hora (osea, si por lo que sea tengo 24 minutos)
    df['Date/Time'] = new[0].str.cat(new[1], sep=" ")
    df['Date/Time'] = df['Date/Time'].str.strip()
    df = df.set_index('Date/Time')
    df.index = pd.to_datetime(df.index, format='%m-%d-%y %H:%M:%S')
    return df


def get_outputs(file, variableName, scheduleName):
    # TODO hacerlo para una lista de variables
    '''
    Create a dataframe from eplusout.eso with the output variable to study
    '''
    os.system(file + '/ReadVarsESO')
    data = pd.read_csv(file + '/eplusout.csv')
    data = data.set_index('Date/Time')
    pattern = re.compile(variableName)
    for i in data.columns:
        if pattern.search(i):  # me dará como resultado todas las thermas zones..
            col = i
    if not col:
        raise Exception(variableName + " ")
    data = data[col].to_frame()
    data.rename(columns={col: ':'.join([col, scheduleName])}, inplace=True)
    return data
