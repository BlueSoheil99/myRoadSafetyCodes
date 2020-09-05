import pandas as pd
import os
import numpy as np

'''
main author: Hesam

'''

main_dir = r'D:\Educational\proje\data\extracted data\time series\Gilan province'

os.chdir(main_dir)
monthly_excel = pd.read_excel(r'90,97.xlsx')  # monthly date Excel in the directory
daily_excel = pd.read_excel(r'raw_police.xlsx')  # filtered Excel with all Crashes and Their Attributes in the directory
police_traffic_excel = pd.read_excel(r'police_traffic.xlsx')  # filtered police_traffic excel in the directory


def yx(a):
    b = a.split("/")
    return b[0]


def mx(a):
    b = a.split("/")
    return b[1]


def state_accumulator(monthly_dataframe, daily_dataframe):
    #todo consider about adding traffic data
    Accident = daily_dataframe['accident'].tolist()
    Month = monthly_dataframe['Month'].tolist()
    Year = monthly_dataframe['Year'].tolist()
    Date = daily_dataframe['date'].tolist()

    yearD = []  # month of each row from daily police traffic
    monthD = []  # month of each row from daily police traffic

    for i in range(len(Date)):  # all data are put in nests of each day via the daily "start" data
        yearD.append(int(yx(Date[i])))
        monthD.append(int(mx(Date[i])))

    crashes, summ = [[] for i in Month], []

    for i in range(len(Month)):
        for j in range(len(monthD)):
            if yearD[j] == Year[i] and Month[i] == monthD[j]:
                crashes[i].append(Accident[j])
    for i in crashes:
        for j in range(len(i)):
            if np.isnan(i[j]):
                i[j] = 0
        accidents = sum(i)
        summ.append(accidents)

    # data = {'Crashes': crashes, 'Accidents': summ}
    # data = {'Accidents': summ}
    df = pd.DataFrame({'Accidents': summ})
    # df.to_excel(r'D:\Educational\proje\data\extracted data\time series\Tehran province\soup.xlsx')
    return df


def cause_accumulator(monthly_dataframe, daily_dataframe):
    Cause = daily_dataframe['cause'].tolist()
    Month = monthly_dataframe['Month'].tolist()
    Year = monthly_dataframe['Year'].tolist()
    Date = daily_dataframe['date'].tolist()

    yearD = []  # month of each row from daily police traffic
    monthD = []  # month of each row from daily police traffic

    for i in range(len(Date)):  # all data are put in nests of each day via the daily "start" data
        yearD.append(int(yx(Date[i])) + 1300)
        monthD.append(int(mx(Date[i])))

    k0, k1 = [[] for i in Month], []
    cause_list = list(set(Cause))

    for i in range(len(Month)):
        for j in range(len(monthD)):
            if yearD[j] == Year[i] and Month[i] == monthD[j]:
                k0[i].append(Cause[j])

    b = [[] for i in k0]

    # k1 = [len(i) for i in k0]
    for j in range(len(k0)):
        for i in range(len(cause_list)):
            b[j].append(k0[j].count(cause_list[i]))

    df = pd.DataFrame(b, columns=cause_list)
    # df.to_excel('soup2.xlsx')
    return df


state_sum = state_accumulator(monthly_excel, police_traffic_excel)
state_causes = cause_accumulator(monthly_excel, daily_excel)
new_data = pd.concat([monthly_excel, state_sum, state_causes], axis=1)

new_data.to_excel('model_data.xlsx', index=False)
