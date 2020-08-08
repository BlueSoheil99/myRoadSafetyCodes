import pandas as pd
import numpy as np
from scipy.stats import skew
import os

os.chdir(r'D:\Educational\proje\data')
input_address = r'traffic\gilan95\543451-95-AstanehToLahijan.xlsx'
routeCode = '543451'

output_address = input_address[:-5] + '-proff.xlsx'
Traffic = pd.read_excel(input_address)
########################
########################
Start = Traffic['start'].tolist()
End = Traffic['end'].tolist()
TotalObserved = Traffic['total observed'].tolist()
TotalEstimated = Traffic['total estimated'].tolist()
Avg_s = Traffic['avg. Speed'].tolist()
class1 = Traffic['class1'].tolist()
class2 = Traffic['class2'].tolist()
class3 = Traffic['class3'].tolist()
class4 = Traffic['class4'].tolist()
class5 = Traffic['class5'].tolist()
dis_vio = Traffic['distance violation'].tolist()
speed_vio = Traffic['speed violation'].tolist()
over_vio = Traffic['overtaking violation'].tolist()
########################
########################
Dates = []
AverageSpeeds = []
SpeedVariation = []
DailyTraffic = []
DT_variation = []
TruckPercentages = []
SpeedSkewness = []
DT_Skewness = []
########################
########################
currentDate = ''
hours = 0
totalVehicles = []
totalHeavyVehicles = []
speeds = []
Code = []
########################
########################
days_with_missing_hours = []
days_with_missing_minutes = []


# todo : don't forget to fix missing values
########################
########################

# to extract time and date from traffic data
def dx(a):
    b = a.split(" ")
    return b[0]


def sum_of_heavy_vehicles(row):
    return class2[row] + class3[row] + class4[row] + class5[row]


def handle_previous_date():
    Code.append(routeCode)
    Dates.append(currentDate)
    DailyTraffic.append(np.sum(totalVehicles))
    TruckPercentages.append(round(np.sum(totalHeavyVehicles) / np.sum(totalVehicles) * 100, 2))
    DT_variation.append(round(np.var(totalVehicles)))
    AverageSpeeds.append(round(np.mean(speeds), 2))  # todo: weight mean
    SpeedVariation.append(round(np.var(speeds), 2))
    SpeedSkewness.append(skew(speeds))
    DT_Skewness.append(skew(totalVehicles))


# def weighted_avg_and_std(values, weights):
#     """
#     Return the weighted average and standard deviation.
#
#     values, weights -- Numpy ndarrays with the same shape.
#     """
#     average = np.average(values, weights=weights)
#     # Fast and numerically precise:
#     variance = np.average((values - average) ** 2, weights=weights)
#     return (average, math.sqrt(variance))


def add_info_to_daily_details(rowNumber, selectedDate):
    totalVehicles.append(TotalEstimated[rowNumber])
    totalHeavyVehicles.append(sum_of_heavy_vehicles(rowNumber))
    speeds.append(Avg_s[rowNumber])
    if TotalEstimated[rowNumber] != TotalObserved[rowNumber]:
        if days_with_missing_minutes.count(selectedDate) == 0:
            days_with_missing_minutes.append(selectedDate)


########################
########################

for i in range(len(Start)):
    selectedDate = dx(Start[i])
    if selectedDate == currentDate:
        add_info_to_daily_details(i, selectedDate)
        hours += 1
    else:
        if currentDate != '':
            if hours != 24:
                days_with_missing_hours.append(currentDate)
            handle_previous_date()
            # clear_lists
            currentDate = ''
            hours = 0
            totalVehicles = []
            totalHeavyVehicles = []
            speeds = []
        currentDate = selectedDate
        add_info_to_daily_details(i, selectedDate)
        hours = 1

print("missing hours in:\n", days_with_missing_hours)
print("missing minutes in:\n", days_with_missing_minutes)

data = pd.DataFrame(
    {'Code': Code, 'Date': Dates, 'DailyTraffic': DailyTraffic, 'DT_variation': DT_variation,
     'DT_skewness': DT_Skewness, 'TruckPercentage': TruckPercentages, 'AverageSpeed': AverageSpeeds,
     'SpeedVariation': SpeedVariation, 'SpeedSkewness': SpeedSkewness})

# data.to_excel(output_address)
