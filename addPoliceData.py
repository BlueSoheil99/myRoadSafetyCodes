import pandas as pd
import numpy as np
from openpyxl import load_workbook
import dateAndTimeGenerator
import os

police_and_traffic_dir = r'D:\Educational\proje\data\extracted data\rasht-lahijan'
route_code = '543110'


def find_traffic_dir(code):
    files_list = os.listdir()
    for i in range(len(files_list)):
        if code in files_list[i] and 'pro.xlsx' in files_list[i]:
            return files_list[i]


def find_police_dir(code):
    files_list = os.listdir()
    for i in range(len(files_list)):
        if code in files_list[i] and 'police.xlsx' in files_list[i]:
            return files_list[i]


def aggregate_police_data(police_path):
    data = pd.read_excel(police_path, sheet_name='processed')
    year = '13' + police_path[7:9]  # police path format: $$$$$$-$$-routeDirection-police.xlsx
    dates = dateAndTimeGenerator.get_full_dates_of_a_year(year)
    multi, single, not_severe, severe = dict(), dict(), dict(), dict()
    for date in dates:
        multi[date] = 0
        single[date] = 0
        not_severe[date] = 0
        severe[date] = 0

    def get_date_in_string(police_date):
        police_date = police_date.split('/')
        day = police_date[2]
        month = police_date[1]
        year = police_date[0]
        if len(day) == 1:
            day = '0' + day
        if len(month) == 1:
            month = '0' + month
        if len(year) == 2:
            year = '13' + year
        return '/'.join([year, month, day])

    for index, row in data.iterrows():
        date = get_date_in_string(row['تاريخ تصادف'])
        multi[date] += row['multi']
        single[date] += row['single']
        not_severe[date] += row['property']
        severe[date] += row['severe']

    total_crashes, multi_crashes, single_crashes, not_severe_crashes, severe_crashes = [[] for i in range(5)]
    for i in range(len(dates)):
        multi_crashes.append(multi[dates[i]])
        single_crashes.append(single[dates[i]])
        severe_crashes.append(severe[dates[i]])
        not_severe_crashes.append(not_severe[dates[i]])
        total_crashes.append(multi_crashes[i] + single_crashes[i])

    new_data = pd.DataFrame({'date': dates, 'total crashes': total_crashes, 'single vehicle crashes': single_crashes,
                             'multi vehicle crashes': multi_crashes, 'property damage only crashes': not_severe_crashes,
                             'injury crashes': severe_crashes, })
    # saving a new sheet in police excel file
    book = load_workbook(police_path)
    writer = pd.ExcelWriter(police_path, engine='openpyxl')
    writer.book = book
    new_data.to_excel(writer, sheet_name='aggregated')
    writer.save()
    writer.close()


def merge_police_and_traffic(police_path, traffic_path):
    police_data = pd.read_excel(police_path, sheet_name='aggregated')
    traffic_data = pd.read_excel(traffic_path)

    new_data = pd.DataFrame()
    new_data.to_excel(traffic_path)


os.chdir(police_and_traffic_dir)
police_dir = find_police_dir(route_code)
traffic_dir = find_traffic_dir(route_code)
aggregate_police_data(police_dir)
# merge_police_and_traffic(police_dir, traffic_dir)
