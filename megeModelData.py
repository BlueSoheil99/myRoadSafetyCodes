import pandas as pd
import os

'''
this file merges models of all sections in data_path
'''
data_path = r'D:\Educational\proje\data\extracted data\rasht-lahijan\finals for 99.6.4'


def make_a_soup(path):
    files = [i for i in os.listdir(path)]
    dataframes = [pd.read_excel(path + "\\" + i) for i in files]

    for df in dataframes:
        df.drop(df.columns[0], axis=1, inplace=True)

    for i in range(len(dataframes) - 1):
        for index, row in dataframes[i].iterrows():
            if row.tolist().count('Code') > 0:  # for first rows
                data = data.drop([index])
                break

    data = pd.concat(dataframes)
    data.reset_index(drop=True, inplace=True)
    return data


def specify_segment_dummy(dataframe):
    # calculate segment dummies (add <<#of segments -1 >>dummy variables)
    # each way has a dummy segment not each side

    codes = dataframe['Code'].values
    routes = {'Rasht/Kouchesfahan': (543110, 543160), 'Astaneh/Lahijan': (543451, 543401),
              'Kouchesfahan/Astaneh': (543404, 543454)}
    r_k = [0 for i in codes]
    k_a = [0 for i in codes]
    a_l = [0 for i in codes]
    for i in range(len(codes)):
        if codes[i] in routes['Rasht/Kouchesfahan']:
            r_k[i] = 1
            continue
        if codes[i] in routes['Kouchesfahan/Astaneh']:
            k_a[i] = 1
            continue
        elif codes[i] in routes['Astaneh/Lahijan']:
            a_l[i] = 1
            continue

    segment_dataframe = pd.DataFrame({'Rasht/Kouchesfahan': r_k, 'Astaneh/Lahijan': a_l, 'Kouchesfahan/Astaneh': k_a})

    segment_dataframe.drop(segment_dataframe.columns[0], axis=1, inplace=True)
    # as we need <<#of segments -1 >>dummy variables, we intentionally drop one of columns of segment_dataframe
    new_data = pd.concat([segment_dataframe, dataframe], axis=1)
    return new_data


soup = make_a_soup(data_path)
soup = specify_segment_dummy(soup)
soup.to_excel(data_path + r'\model_soup.xlsx')
