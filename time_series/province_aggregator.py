import pandas as pd
import os

'''
this code merges all crashes of selected provinces into one single excel file

'''
# todo rearrange all dataframes
province_name = 'گیلان'
output_name = 'gilan_police.xlsx'
_dir = r'D:\Educational\proje\data\police'
input_directory = 'similar police data'
# input directory should contain ONLY one-year police excel source_dataframes in ONE specific format.
output_directory = 'extracted data'
police_database_address = r'police'

os.chdir(_dir)
dataframes_to_concat = []
source_dataframes = [pd.read_excel(i) for i in os.listdir(input_directory)]
# wait for an hour to fully execute this shit:)


for dataframe in source_dataframes:  # filtering data
    for index, row in dataframe.iterrows():
        if row['استان'] != province_name and row['استان'] != 'استان':
            dataframe = dataframe.drop([index])
    dataframes_to_concat.append(dataframe)  # check this dataframe wont change in next iterations


for i in range(len(dataframes_to_concat)-1):
    dataframe = dataframes_to_concat[i+1]
    dataframe.drop(dataframe.index[0])
    # DFs have columns name in their 1st row and except for the 1st DF, others are extra


data = pd.concat(dataframes_to_concat)
data.reset_index(drop=True, inplace=True)
data.to_excel(output_name)
