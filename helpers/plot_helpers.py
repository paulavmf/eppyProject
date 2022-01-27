import matplotlib.pyplot as plt
from helpers.idf_helpers import *

'''
period  = [ 'init' , 'end']
env_data = env_data
data_to_compare = [data1,data2,data2..]
title = [title1,title2,title3]
'''


def overlay_timeseries(p, env_data, data_list, titles):
    plt.figure(figsize=(12, 5))
    ax = []

    for i, data in enumerate(data_list):
        ax.append(data[p[0]:p[1]].plot(grid=True, label=titles[i]))
    ax.append(
        env_data[p[0]:p[1]].plot(linestyle='--', color='black', grid=True, secondary_y=True, label='Env Temperature')
    )

    h1, l1 = ax[-1].get_legend_handles_labels()
    h2, l2 = ax[-2].get_legend_handles_labels()
    # TODO DE ESTA MANERA PUEDE PONER EJES DISTINTOS A LA IQ Y A LA DCHA
    plt.legend(h1 + h2, l1 + l2, loc=0)
    return (plt)


def merge_transform_ts(p, env_data, data_list, titles):
    env_data = env_data[p[0]:p[1]]
    for index, data in enumerate(data_list):
        data_list[index] = data[p[0]:p[1]].to_frame()
        data_list[index].rename(columns={data_list[index].columns[0]: data_list[index].columns[0] + titles[index]}, inplace=True)
    newdata = data_list[0]
    for i, data in enumerate(data_list[1:]):
        i += 1
        newdata = newdata.merge(data, on = 'Date/Time')
    newdata = newdata.merge(env_data,  on = 'Date/Time')
    return (newdata)

def schedule_to_ts(idf, schedules_name):
    import os
    from shutil import copyfile
    for obj in idf.idfobjects['OUTPUT:VARIABLE']:
        idf.removeidfobject(obj)
    for schedule_name in schedules_name:
        idf.newidfobject('OUTPUT:VARIABLE')
        idf.idfobjects['OUTPUT:VARIABLE'][-1].Key_Value = schedule_name
        idf.idfobjects['OUTPUT:VARIABLE'][-1].Variable_Name = 'Schedule Value'
    # TODO THIS DOES NOT WORK
    try:
        os.mkdir('tmp')
    except FileExistsError:
        print("Directory already exists")

    print(idf.idfobjects['OUTPUT:VARIABLE'])
    idf.saveas('tmp/idf')
    copyfile('/home/paula/Documentos/Doctorado/Desarrollo/eppyProject/studies/ReadVarsESO','tmp/ReadVarsESO')
    os.system('tmp/ReadVarsESO')
    data = eso_to_ts('tmp/eplusout.csv')
    return(data)

