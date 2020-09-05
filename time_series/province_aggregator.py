import pandas as pd
import os

'''
this code merges all crashes of selected provinces into one single excel file

'''

province_name = 'گيلان'
output_name = 'gilan_police.xlsx'

_dir = r'D:\Educational\proje\data\police'
input_directory = 'similar police data'
# input directory should contain ONLY one-year police excel source_dataframes in ONE specific format.
output_directory = 'extracted data'
police_database_address = r'police'

os.chdir(_dir)
dataframes_to_concat = []
source_dataframes = [pd.read_excel(input_directory + '\\' + i) for i in os.listdir(input_directory)]
# wait for an hour to fully execute this shit:)
# source_dataframes = []
# listam = os.listdir(input_directory)
# for i in listam:
#     print(i)
#     source_dataframes.append(pd.read_excel(input_directory+'\\'+i))
#     print(i + ' is added to dataframes')  # it's just for logging
# source_dataframes.append(pd.read_excel(listam[0]))


for dataframe in source_dataframes:  # filtering data
    for index, row in dataframe.iterrows():

        # debug log started
        ostan = row['استان']
        if type(ostan) != str:
            continue
        print(ostan, province_name, province_name == ostan)
        print(type(ostan), len(ostan))
        print(type(province_name), len(province_name))
        #debug log ended

        if row['استان'] != province_name and row['استان'] != 'استان':
            # print('a row with '+row['استان'] + ' was deleted')
            dataframe = dataframe.drop([index])
    dataframes_to_concat.append(dataframe)  # check this dataframe wont change in next iterations

for i in range(len(dataframes_to_concat) - 1):
    dataframe = dataframes_to_concat[i + 1]
    dataframe.drop(dataframe.index[0])
    # DFs have columns name in their 1st row and except for the 1st DF, others are extra

data = pd.concat(dataframes_to_concat)
data.reset_index(drop=True, inplace=True)
data.to_excel(output_directory + '\\' + output_name)
