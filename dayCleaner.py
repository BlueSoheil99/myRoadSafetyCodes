import pandas as pd
import numpy as np
import dateAndTimeGenerator


def clean_dataset(dataframe):
    ######## adjusting missed minutes #########
    for index, row in dataframe.iterrows():
        if row['total observed'] != row['total estimated']:
            row = hourly_adjust(row)

    ######## extraction of dataFrame data #########
    Code, Mehvar = dataframe['code'].tolist(), dataframe['mehvar'].tolist()
    start, end = dataframe['start'].tolist(), dataframe['end'].tolist()
    interval = dataframe['interval'].tolist()
    total_observed, total_estimated = dataframe['total observed'].tolist(), dataframe['total estimated'].tolist()
    class1, class2, class3, class4, class5 = dataframe['class1'].tolist(), dataframe['class2'].tolist(), dataframe[
        'class3'].tolist(), dataframe['class4'].tolist(), dataframe['class5'].tolist()
    avg_s = dataframe['avg. Speed'].tolist()
    dis_vio, speed_vio, over_vio = dataframe['distance violation'].tolist(), dataframe['speed violation'].tolist(), \
                                   dataframe['overtaking violation'].tolist()

    ######## setup new lists to make a new frameWork #########
    new_start = dateAndTimeGenerator.get_date_and_times_in_a_period(start[0], start[-1])
    new_end = new_start[1:]
    new_start = new_start[:-1]
    new_interval, new_total_observed, new_total_estimated, new_avg_s, new_class1, new_class2, new_class3, \
    new_class4, new_class5, new_dis_vio, new_speed_vio, new_over_vio = [[0] * len(new_start) for i in range(12)]

    ######## replace valid data in new lists #########
    for i in range(len(start)):
        if start[i] in new_start:
            j = new_start.index(start[i])
            new_interval[j] = interval[i]
            new_total_observed[j], new_total_estimated[j] = total_observed[i], total_estimated[i]
            new_avg_s[j] = avg_s[i]
            new_class1[j], new_class2[j], new_class3[j], new_class4[j], new_class5[j] = class1[i], class2[i], class3[i], \
                                                                                        class4[i], class5[i]
            new_dis_vio[j], new_speed_vio[j], new_over_vio[j] = dis_vio[i], speed_vio[i], over_vio[i]

    ######## cleat invalid data in new lists #########
    #todo: check when a month a missed
    for i in range(len(new_total_estimated)):
        if new_total_estimated[i] == 0:  # this indicates an empty hour with zero values
            dt_b, dt_a = 0, 0
            class1_b, class1_a = 0, 0
            class2_b, class2_a = 0, 0
            class3_b, class3_a = 0, 0
            class4_b, class4_a = 0, 0
            class5_b, class5_a = 0, 0
            avg_s_b, avg_s_a = 0, 0
            speed_vio_b, speed_vio_a = 0, 0
            over_vio_b, over_vio_a = 0, 0
            dis_vio_b, dis_vio_a = 0, 0

            for j in [168, 167, 169]:  # 7*24 hour = 168
                if i + j < len(new_total_estimated) and new_total_estimated[i + j] != 0:
                    # this shows that we have the data of such hour for next week in the same weekday(1day tolerance)
                    dt_a = new_total_estimated[i + j]
                    class1_a, class2_a, class3_a = new_class1[i + j], new_class2[i + j], new_class3[i + j]
                    class4_a, class5_a = new_class4[i + j], new_class5[i + j]
                    avg_s_a = new_avg_s[i + j]
                    speed_vio_a, over_vio_a, dis_vio_a = new_speed_vio[i + j], new_over_vio[i + j], new_dis_vio[i + j]
                    break
            for j in [168, 167, 169]:
                if i - j > 1 and new_total_estimated[i - j] != 0:
                    # this shows we have the data of such hour for previous week in the same weekday(1day tolerance)
                    dt_b = new_total_estimated[i - j]
                    class1_b, class2_b, class3_b = new_class1[i - j], new_class2[i - j], new_class3[i - j]
                    class4_a, class5_b = new_class4[i - j], new_class5[i - j]
                    avg_s_b = new_avg_s[i - j]
                    speed_vio_b, over_vio_b, dis_vio_b = new_speed_vio[i - j], new_over_vio[i - j], new_dis_vio[i - j]
                    break

            if dt_a != 0 and dt_b != 0:
                new_class1[i] = int((class1_b + class1_a) / 2)
                new_class2[i] = int((class2_b + class2_a) / 2)
                new_class3[i] = int((class3_b + class3_a) / 2)
                new_class4[i] = int((class4_b + class4_a) / 2)
                new_class5[i] = int((class5_b + class5_a) / 2)
                new_speed_vio[i] = int((speed_vio_b + speed_vio_a) / 2)
                new_over_vio[i] = int((over_vio_b + over_vio_a) / 2)
                new_dis_vio[i] = int((dis_vio_b + dis_vio_a) / 2)
                new_avg_s[i] = round(np.average([avg_s_b, avg_s_a], weights=[dt_b, dt_a]), 2)

            elif dt_a != 0:
                new_class1[i] = class1_a
                new_class2[i] = class2_a
                new_class3[i] = class3_a
                new_class4[i] = class4_a
                new_class5[i] = class5_a
                new_speed_vio[i] = speed_vio_a
                new_over_vio[i] = over_vio_a
                new_dis_vio[i] = dis_vio_a
                new_avg_s[i] = avg_s_a
            elif dt_b != 0:
                new_class1[i] = class1_b
                new_class2[i] = class2_b
                new_class3[i] = class3_b
                new_class4[i] = class4_b
                new_class5[i] = class5_b
                new_speed_vio[i] = speed_vio_b
                new_over_vio[i] = over_vio_b
                new_dis_vio[i] = dis_vio_b
                new_avg_s[i] = avg_s_b

            new_total_estimated[i] = new_class1[i] + new_class2[i] + new_class3[i] + new_class4[i] + new_class5[i]

    ######## making a new frameWork #########
    Code = [Code[0]] * len(new_start)
    Mehvar = [Mehvar[0]] * len(new_start)
    new_dataframe = pd.DataFrame(
        {'code': Code, 'mehvar': Mehvar, 'start': new_start, 'end': new_end, 'interval': new_interval,
         'total observed': new_total_observed, 'class1': new_class1, 'class2': new_class2, 'class3': new_class3,
         'class4': new_class4, 'class5': new_class5, 'avg. Speed': new_avg_s, 'speed violation': new_speed_vio,
         'distance violation': new_dis_vio, 'overtaking violation': new_over_vio,
         'total estimated': new_total_estimated})
    return new_dataframe


def hourly_adjust(row):
    """
    in this method we don't change the intervals and total observations and avg.speed
    but other values will be adjusted for a 60min interval
    """
    interval = row['interval']
    row['speed violation'] = round(row['speed violation'] * 60 / interval)
    row['overtaking violation'] = round(row['overtaking violation'] * 60 / interval)
    row['distance violation'] = round(row['distance violation'] * 60 / interval)
    row['class1'] = round(row['class1'] * 60 / interval)
    row['class2'] = round(row['class2'] * 60 / interval)
    row['class3'] = round(row['class3'] * 60 / interval)
    row['class4'] = round(row['class4'] * 60 / interval)
    row['class5'] = round(row['class5'] * 60 / interval)
    row['total estimated'] = row['class1'] + row['class2'] + row['class3'] + row['class4'] + row['class5']
    return row

########## test and debug code start ####################

# print(are_dates_equal([2017, 3, 5], [2017, 3, 5]))
# print(are_times_equal([23, 45], [23, 45]))
# print(dateAndTimeGenerator.get_date_and_times_in_a_period('1395/03/21 23:00:00', '1396/03/21 15:00:00'))

########## test and debug code end   ####################
