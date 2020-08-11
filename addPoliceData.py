import pandas as pd
from openpyxl import load_workbook
import dateAndTimeGenerator
import os

# TODO: appending seasons and holiday happens here. write the code and
#  change the file name into addPoliceAndHolidayData.py later

"""
to use this code first you need to have both traffic and police data in same folder just like 
'543110-95-RashtToKouchesfahan-police.xlsx' and '543110-95-RashtToKouchesfahan-pro.xlsx' present in code directory,
make traffic daily data using other codes here but then add holidays,seasons,road geometrics manually.
also making police worksheets should also be handled manually

"""

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
    # police_data = pd.read_excel(police_path, sheet_name='aggregated', usecols="C:G")
    # traffic_data = pd.read_excel(traffic_path, usecols="B:Y")
    # to use 'usecols=",,," ' we should be always be aware of police and traffic data attributes(if we decide to add or
    # remove a column in making these databases, we should adjust lines above too) but with drop
    police_data = pd.read_excel(police_path, sheet_name='aggregated')
    traffic_data = pd.read_excel(traffic_path)
    police_data.drop(police_data.columns[0:2], axis=1, inplace=True)
    traffic_data.drop(traffic_data.columns[0], axis=1, inplace=True)

    new_data = pd.concat([traffic_data, police_data], axis=1)
    new_data.to_excel(traffic_path)


# def aggregate_police_data_and_merge_with_traffic(police_and_traffic_dir, route_code):
os.chdir(police_and_traffic_dir)
police_dir = find_police_dir(route_code)
traffic_dir = find_traffic_dir(route_code)
aggregate_police_data(police_dir)
merge_police_and_traffic(police_dir, traffic_dir)
