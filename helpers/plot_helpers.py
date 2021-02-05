import matplotlib.pyplot as plt


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
        env_data[p[0]:p[1]].plot(linestyle='--', color='black', grid=True, secondary_y=True, label='Env Temperature'))

    h1, l1 = ax[-1].get_legend_handles_labels()
    h2, l2 = ax[-2].get_legend_handles_labels()
    # TODO esta movida del handles labels no sé cómo es
    plt.legend(h1 + h2, l1 + l2, loc=0)