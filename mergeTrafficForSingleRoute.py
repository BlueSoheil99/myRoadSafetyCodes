import os
import pandas as pd
import dayCleaner

os.chdir(r'D:\Educational\proje\data')
province_dir = r'traffic\gilan95'
goal = 'Hourly 543160'  # specified text that we look for in file names
output_address = province_dir + r'\543160-95-KouchesfahanToRasht-تست.xlsx'

list_of_goal_files = []
files = os.walk(province_dir + r'\raw data')  # location of the main Folder of raw data
for folder in files:
    for file in folder[2]:
        if goal in file:
            list_of_goal_files.append(folder[0] + '\\' + file)

combination = []
for file in list_of_goal_files:
    combination.append(pd.read_excel(file))

data = pd.concat(combination, ignore_index=True)
data.columns = ['code', 'mehvar', 'start', 'end', 'interval', 'total observed', 'class1', 'class2', 'class3', 'class4',
                'class5', 'avg. Speed', 'speed violation', 'distance violation', 'overtaking violation',
                'total estimated']

for index, row in data.iterrows():
    if row.tolist().count('کد محور') > 0:
        data = data.drop([index])

data.reset_index(drop=True, inplace=True)

data = dayCleaner.clean_dataset(data)

data.to_excel(output_address)
