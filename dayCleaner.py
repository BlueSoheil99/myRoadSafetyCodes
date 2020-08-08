import pandas as pd
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
    new_interval, new_total_observed, new_total_estimated, new_avg_s, new_class1, new_class2, \
    new_class3, new_class4, new_class5, new_dis_vio, new_speed_vio, new_over_vio = [[0] * len(new_start) for i in
                                                                                    range(12)]
    ######## setup new lists to make a new frameWork #########
    # for i in range(len(start)):
    #     if start[i] in new_start:
    #         j = new_start.index(start[i])
    #         misseddate[j] = start[i]
    #         missedHT[j] = HT[i]
    #         missedclass1[j] = class1[i]
    #         missedspeed[j] = speed[i]

    # new_dataframe = pd.DataFrame(
    #     {'code': Code, 'mehvar': Mehvar, 'start': new_start, 'end': new_end, 'interval': new_interval,
    #      'total observed': new_total_observed, 'class1': new_class1, 'class2': new_class2, 'class3': new_class3,
    #      'class4': new_class4, 'class5': new_class5, 'avg. Speed': new_avg_s, 'speed violation': new_speed_vio,
    #      'distance violation': new_dis_vio, 'overtaking violation': new_over_vio,
    #      'total estimated': new_total_estimated})
    # return new_dataframe
    return dataframe


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


def date_extractor(dateAndTime):
    ans_list = dateAndTime.split(" ")
    ans_list = ans_list[0].split("/")
    return ans_list


def time_extractor(dateAndTime):
    ans_list = dateAndTime.split(" ")
    ans_list = ans_list[1].split(":")
    return ans_list


def are_times_equal(timeList1, timeList2):
    for i in range(len(timeList2)):  # both time lists must have similar length(we just use hour and minute(len=2))
        if timeList1[i] != timeList2[i]:
            return False
    return True


def are_dates_equal(dateList1, dateList2):
    for i in range(3):  # both dateLists must have similar length(3)
        if dateList1[i] != dateList2[i]:
            return False
    return True

########## test and debug code start ####################

# print(are_dates_equal([2017, 3, 5], [2017, 3, 5]))
# print(are_times_equal([23, 45], [23, 45]))
# print(dateAndTimeGenerator.get_date_and_times_in_a_period('1395/03/21 23:00:00', '1396/03/21 15:00:00'))

########## test and debug code end   ####################
