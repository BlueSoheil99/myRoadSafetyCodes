import os

import dbscan1d as dbscan1d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot


def scan(dataframe):
    # clean_dataframe = dataframe
    dt_index = dataframe.columns.values.tolist().index('DailyTraffic')
    date_index = dataframe.columns.values.tolist().index('Date')
    DTs = dataframe.iloc[:, [dt_index]].values
    dates = dataframe.iloc[:, [date_index]].values
    # DTs = dataframe['DailyTraffic'].values
    # dates = dataframe['Date'].values

    list_of_outlier_dates = get_dbscan_outliers(DTs, dates)
    # list_of_outlier_dates = scan_fbprophet(DTs, dates)
    new_dataframe = clean_outliers(dataframe, list_of_outlier_dates)

    return new_dataframe


def get_dbscan_outliers(DTs, dates):
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler, normalize

    scaler = StandardScaler()
    # DTs_norm = normalize(DTs_scaled)
    days_and_DTs = [[i, DTs[i]] for i in range(len(dates))]
    two_d_array_scaled = scaler.fit_transform(days_and_DTs)  # normalizing both columns(day and daily traffic)

    dbscan = DBSCAN(eps=0.5, min_samples=4)

    labels = dbscan.fit(two_d_array_scaled).labels_
    outlier_dates_list = []
    Noises = dict()
    Clusters = dict()
    Boundarys = dict()
    for i in range(len(DTs)):
        if labels[i] == -1:
            Noises[two_d_array_scaled[i, 0]] = two_d_array_scaled[i, 1]
            outlier_dates_list.append(dates[i])
        elif labels[i] == 0:
            Boundarys[two_d_array_scaled[i, 0]] = two_d_array_scaled[i, 1]
        else:
            Clusters[two_d_array_scaled[i, 0]] = two_d_array_scaled[i, 1]

    plot.scatter(Noises.keys(), Noises.values())
    plot.scatter(Clusters.keys(), Clusters.values())
    plot.scatter(Boundarys.keys(), Boundarys.values())
    plot.show()

    return outlier_dates_list


def scan_fbprophet(DTs, dates):
    return None


def clean_outliers(dataframe, dates):
    return dataframe
