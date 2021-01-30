import matplotlib.pyplot as plt

def overlay_timeseries(TitileDataDict):
    for k,v in TitileDataDict:
        ax = v[0].plot(color=v[1], grid=True, label=k)
        # TODO terminar esto para que acepte el dash y tal... mirar el tema de args y kwargs y hacerlo e otra forma
        pass
