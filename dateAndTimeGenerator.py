import pandas as pd
from ordered_set import OrderedSet  # https://pypi.org/project/ordered-set/
import os

os.chdir(r"D:\Educational\proje\data")


def create_full_times():
    sample = pd.read_excel('fullTimesSample.xlsx', header=None)  # sample should have full times of one month
    sample = sample[0].tolist()

    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    years = ['1390', '1391', '1392', '1393', '1394', '1395', '1396', '1397']
    kabise_years = ['1391', '1395']

    full_times_for_a_year = []
    for month_index in range(12):
        for date in sample:
            part1, part2, part3 = date.split('/')
            part2 = months[month_index]
            if not (month_index > 5 and part3[0:2] == '31'):
                full_times_for_a_year.append('/'.join([part1, part2, part3]))

    full_times = []
    for year_index in range(8):
        for date in full_times_for_a_year:
            part1, part2, part3 = date.split('/')
            part1 = years[year_index]
            if not (month_index == 11 and part3[0:2] == '30' and part1 not in kabise_years):
                full_times.append('/'.join([part1, part2, part3]))

    data = pd.DataFrame(full_times)
    data.to_excel('fullTimes.xlsx')
    # don't forget to delete the that stupid first row and column in output file manually !


def get_date_and_times_in_a_period(startDateAndTime, endDateAndTime):
    """
    parameters should have a syntax like: '1395/02/15 23:00:00'
    :param startDateAndTime:
    :param endDateAndTime:
    :return: a list of full times between specified date and times + 1hour after ending date and time
    """
    date_and_times = pd.read_excel('fullTimes.xlsx', header=None)
    date_and_times = date_and_times[0].tolist()
    index1 = date_and_times.index(startDateAndTime)
    index2 = date_and_times.index(endDateAndTime)
    return date_and_times[index1:index2 + 2]


def get_full_dates_of_a_year(year):
    """
    :param year: a string like : '1395'
    :return: a list of strings containing the outlier_dates in given year
    """
    dates = OrderedSet()
    date_and_times = pd.read_excel(r"D:\Educational\proje\data\fullTimes.xlsx", header=None)
    date_and_times = date_and_times[0].tolist()
    for date_and_time in date_and_times:
        if year in date_and_time:
            dates.add(date_and_time.split(" ")[0])
    list_of_dates = [i for i in dates]
    return list_of_dates
