import os

import matplotlib.pyplot as plt


def scan(dataframe):
    # clean_dataframe = dataframe
    dt_index = dataframe.columns.values.tolist().index('DailyTraffic')
    date_index = dataframe.columns.values.tolist().index('Date')
    DTs = dataframe.iloc[:, [dt_index]].values
    dates = dataframe.iloc[:, [date_index]].values
    # DTs = dataframe['DailyTraffic'].values
    # outlier_dates = dataframe['Date'].values

    list_of_outlier_dates = get_dbscan_outliers(DTs, dates)
    new_dataframe = clean_outliers(dataframe, list_of_outlier_dates)

    return new_dataframe


def get_dbscan_outliers(DTs, dates):
    def get_proper_eps(array_2d):
        e = 0.5
        return e

    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler, normalize

    scaler = StandardScaler()
    days_and_DTs = [[i, DTs[i]] for i in range(len(dates))]
    scaled_array = scaler.fit_transform(days_and_DTs)  # standard normalizing both columns(day and daily traffic)
    scale = (max([scaled_array[i, 1] for i in range(len(scaled_array))]) - min([scaled_array[i, 1] for i in range(len(scaled_array))])) / \
            (max([scaled_array[i, 0] for i in range(len(scaled_array))]) - min([scaled_array[i, 0] for i in range(len(scaled_array))]))
    # todo check it later:  DTs_norm = normalize(DTs_scaled)
    scaled_array = [[scaled_array[i, 0]*scale, scaled_array[i, 1]] for i in range(len(scaled_array))]

    epsilon = get_proper_eps(scaled_array)
    minimum_samples = 5
    dbscan = DBSCAN(eps=epsilon, min_samples=minimum_samples)
    model = dbscan.fit(scaled_array)
    labels = model.labels_

    outlier_dates_list = []
    Noises = dict()
    Clusters = dict()
    for i in range(len(DTs)):
        if labels[i] == -1:
            Noises[scaled_array[i][0]] = scaled_array[i][1]
            outlier_dates_list.append(dates[i][0])

            # clustering is finished,
            # codes below are for showing the result and can be deleted.

        else:
            Clusters[scaled_array[i][0]] = scaled_array[i][1]

    real_noises, real_clusters = dict(), dict()
    for i in range(len(dates)):
        if dates[i][0] in outlier_dates_list:
            real_noises[days_and_DTs[i][0]] = days_and_DTs[i][1]
        else:
            real_clusters[days_and_DTs[i][0]] = days_and_DTs[i][1]

    # let's show scatter plots
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.plot([i[0] for i in days_and_DTs], [i[1] for i in days_and_DTs], 'o', label='given data')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(list(Noises.keys()), list(Noises.values()), 'x', color='red', label='noise')
    plt.plot(list(Clusters.keys()), list(Clusters.values()), 'o', color='green', label='in a cluster')
    plt.xlabel('day# in the year- standard normalized* ')
    plt.ylabel('daily traffic- standard normalized')
    plt.title('DBSCAN with eps=%.2f , min_samples=%d \n SCALED' % (epsilon, minimum_samples))
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(list(real_noises.keys()), list(real_noises.values()), 'x', color='red', label='noise')
    plt.plot(list(real_clusters.keys()), list(real_clusters.values()), 'o', color='green', label='in a cluster')
    plt.xlabel('day# in the year')
    plt.ylabel('daily traffic')
    plt.title('result of outlier detection algorithm')
    plt.legend()

    # plt.show()

    return outlier_dates_list


def scan_multivariate_normal(DTs, dates):
    return None


def clean_outliers(dataframe, outlier_dates):
    count = 0
    data_dict = dict()
    # main code starts.
    for index, row in dataframe.iterrows():
        if row['Date'] in outlier_dates:
            dataframe = dataframe.drop([index])
    # main code ended.
    # other lines could be deleted and are for displaying the trend of cleaning
        else:
            data_dict[count] = row['DailyTraffic']
        count += 1

    axes = plt.gca()
    plot_range = axes.get_ylim()
    plt.subplot(2, 2, 4)
    plt.ylim(plot_range)
    plt.plot(list(data_dict.keys()), list(data_dict.values()), 'o')
    plt.xlabel('day# in the year')
    plt.ylabel('daily traffic')
    plt.title('cleaned data')
    plt.tight_layout()
    plt.show()

    return dataframe
