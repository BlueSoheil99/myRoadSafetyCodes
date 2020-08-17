import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from sklearn.cluster import DBSCAN


def scan(dataframe):
    # clean_dataframe = dataframe
    index = dataframe.columns.values.tolist().index('DailyTraffic')
    date_index = dataframe.columns.values.tolist().index('Date')
    DTs = dataframe.iloc[:, [index]].values
    dates = dataframe.iloc[:, [date_index]].values
    # DTs = dataframe['DailyTraffic'].values
    # dates = dataframe['Date'].values

    dbscan = DBSCAN(eps=1000, min_samples=3)  # eps is defined as diameter of 600 vehicles for DT points
    labels = dbscan.fit(DTs).labels_
    Noises = dict()
    Clusters = dict()
    Boundarys = dict()
    for i in range(len(DTs)):
        date , dt = dates[i][0] , DTs[i][0]
        if labels[i] == -1:
            Noises[i] = dt
        elif labels[i] == 0:
            Clusters[i] = dt
        else:
            Boundarys[i] = dt

    plot.scatter(Noises.keys(), Noises.values())
    plot.scatter(Clusters.keys(), Clusters.values())
    plot.scatter(Boundarys.keys(), Boundarys.values())
    plot.show()

    return dataframe
