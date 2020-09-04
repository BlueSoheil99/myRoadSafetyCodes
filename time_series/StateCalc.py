import pandas as pd
import numpy as np
'''
main author: Hesam

'''


Monthly = pd.read_excel(r'D:\Educational\proje\data\extracted data\time series\Tehran province\90,97.xlsx')
Daily = pd.read_excel(
    r'D:\Educational\proje\data\extracted data\time series\Tehran province\police_traffic_Tehran.xlsx')

Accident = Daily['accident'].tolist()
Month = Monthly['Month'].tolist()
Year = Monthly['Year'].tolist()
Date = Daily['date'].tolist()


def yx(a):
    b = a.split("/")
    return b[0]


def mx(a):
    b = a.split("/")
    return b[1]


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

'''for i in range(len(k)):         #Std Dev
    if len(k[i])>1:
        k2.append((np.average((w[i]-sum[i])**2))**.5)  #Sample
    else:
        k2.append("Nan")

for i in range(len(k)):         #Skewness
    if len(k[i])>2:
        #l.append((j-sum[i])**3/((len(k[i])-1)*(len(k[i])-2))*len(k[i]))
        k3.append(np.average((w[i]-sum[i])**3/k2[i]**3))
    else:
        k3.append("Nan")'''

# crashes: sum of HT, sum: Average of HT, k2: StdDev of HT, k3: Skew of HT, k4: corrected interval or Raw Interval!!

data = {'Crashes': crashes, 'Sum': summ}
df = pd.DataFrame(data)
df.to_excel(r'D:\Educational\proje\data\extracted data\time series\Tehran province\soup.xlsx')
