import pandas as pd
import os

'''
this file merges models of all sections in data_path
'''
data_path = r'D:\Educational\proje\data\extracted data\rasht-lahijan\finals for 21.5.99'
files = [i for i in os.listdir(data_path)]
dataframes = [pd.read_excel(data_path + '\\' + i) for i in files]

for df in dataframes:
    df.drop(df.columns[0], axis=1, inplace=True)

for i in range(len(dataframes) - 1):
    for index, row in dataframes[i].iterrows():
        if row.tolist().count('Code') > 0:  # for first rows
            data = data.drop([index])
            break

data = pd.concat(dataframes)
#todo calculate segment dummies (add <<#of segments -1 >>dummy variables)
data.reset_index(drop=True, inplace=True)
data.to_excel(data_path + r'\model_soup.xlsx')
