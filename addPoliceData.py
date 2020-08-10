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
        pass

    new_data = pd.DataFrame([0, 0, 0])
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
merge_police_and_traffic(police_dir, traffic_dir)
