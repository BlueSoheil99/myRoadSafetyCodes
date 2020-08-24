import os

import matplotlib.pyplot as plt


def scan(dataframe):
    dt_index = dataframe.columns.values.tolist().index('DailyTraffic')
    date_index = dataframe.columns.values.tolist().index('Date')
    DTs = dataframe.iloc[:, [dt_index]].values
    dates = dataframe.iloc[:, [date_index]].values

    list_of_outlier_dates = get_dbscan_outliers(DTs, dates)
    new_dataframe = clean_outliers(dataframe, list_of_outlier_dates)

    return new_dataframe


def get_dbscan_outliers(DTs, dates):
    # todo for now we just evaluate traffic for detect an outlier.check other variables for clustering(in that case we
    #  will evaluate 3d or more dimensional distances instead of 2D distances and new variables will be effective to
    #  determine proper epsilon

    def get_proper_eps(featured_data, diameter):
        """
        this function calculates an epsilon based on standard deviance of different sections of traffic data
        :param featured_data:is preferred to be standard normal for a better understanding of returned epsilon
        :param diameter:maximum number of points that a core point could have as its neighbor. we use it to determine
        the number of sections that the dataset will be split into
        :return: a proper value for epsilon
        """
        # we define a list with difference between each two consecutive member of featured_data.
        differences = []
        for i in range(1, len(featured_data)):
            differences.append(featured_data[i] - featured_data[i - 1])

        # we divide differences list into smaller parts(#of parts is calculated from diameter parameter).
        # the point is to calculate the mean of these lists STDs and this leads us to a promising value for epsilon.
        # i think if we use STD of whole differences list, that'll be high and won't be a proper epsilon value to
        # determine neighbors of a point
        import math
        number_of_lists = math.floor(len(differences)/diameter)
        difference_lists = []
        for i in range(number_of_lists):
            difference_lists.append(differences[0:diameter])
            differences = differences[diameter:]
        for i in differences:
            difference_lists[-1].append(i)

        # now we calculate mean of STDs
        import numpy as np
        standard_deviance_list = [np.std(i) for i in difference_lists]
        x = np.mean(standard_deviance_list)
        # epsilon is a little less than x due to presence of outliers which rise deviance of a list
        e = 0.9*x
        return round(e, 2)

    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    days_and_DTs = [[i, DTs[i]] for i in range(len(dates))]
    # days_and_DTs helps us to show plot titled:result of outlier detection algorithm
    scaled_array = scaler.fit_transform(DTs)
    # standard normalizing daily traffic. this is optional but normal numbers instead of high ordered numbers...
    # ...helps us to have a better understanding of how the algorithm works

    day_radius = 15
    minimum_samples = 5  # i'm not sure if this is a good number or not
    epsilon = get_proper_eps([i[0] for i in scaled_array], day_radius*2)
    # now we define a 2D array to be clustered by DBSCAN, first column will be scaled #of day and second column will be
    # the standard normalized values that we are already familiar with. day numbers are scaled in a way that the
    # difference between two consecutive days will epsilon/day_radius instead of 1 unit. this way each point will check
    # exactly as much as day_radius*2 points at its neighborhood to see whether they're in a cluster or not.
    scaled_array = [[i*epsilon/day_radius, scaled_array[i][0]] for i in range(len(scaled_array))]

    dbscan = DBSCAN(eps=epsilon, min_samples=minimum_samples)
    model = dbscan.fit(scaled_array)
    labels = model.labels_

    outlier_dates_list = []
    noises = dict()
    clusters = dict()
    for i in range(len(DTs)):
        if labels[i] == -1:
            noises[scaled_array[i][0]] = scaled_array[i][1]
            outlier_dates_list.append(dates[i][0])

            # clustering is finished,
            # lines below are for showing the result and can be deleted or commented.

        else:
            clusters[scaled_array[i][0]] = scaled_array[i][1]

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
    plt.plot(list(noises.keys()), list(noises.values()), 'x', color='red', label='noise')
    plt.plot(list(clusters.keys()), list(clusters.values()), 'o', color='green', label='in a cluster')
    plt.xlabel('day# in the year- scaled to eps/%d  (%d:day radius) ' % (day_radius, day_radius))
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


def clean_outliers(dataframe, outlier_dates):
    count = 0
    data_dict = dict()

    # main code starts here...
    for index, row in dataframe.iterrows():
        if row['Date'] in outlier_dates:
            dataframe = dataframe.drop([index])
    # ...main code ends here.

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


def scan_multivariate_normal(DTs, dates):
    return None


def scan_based_on_other_segments(DTs, dates):
    # if you decided to implement this code, the scan function should be called after road segments merged.
    # and i'm not sure how to write the algorithm:/
    return None