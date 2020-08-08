import pandas as pd
import dateAndTimeGenerator


def clean_dataset(dataframe):
    # todo: get_date_and_times_in_a_period(startDate , startTime , endDate , endTime) from the first until the last of dataFrame

    for index, row in dataframe.iterrows():
        if row['total observed'] != row['total estimated']:
            row['total estimated'] = get_an_estimation(row)


    # newDataframe = pd.DataFrame()
    # newDataframe.columns = dataframe.columns
    return dataframe


def get_an_estimation(row):
    # todo make current estimations for all classes and speed
    # if row['interval'] != 60:
    return round(row['total observed'] * 60 / row['interval'])


# def get_date_and_times_in_a_period(startDate, startTime, endDate, endTime):
#     startDate = [int(i) for i in startDate.split("/")]
#     endDate = [int(i) for i in endDate.split("/")]
#     startTime = [int(i) for i in startTime.split(":")]
#     endTime = [int(i) for i in endTime.split(":")]
#
#     ans_list = []
#     return ans_list


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

print(are_dates_equal([2017, 3, 5], [2017, 3, 5]))
print(are_times_equal([23, 45], [23, 45]))
print(dateAndTimeGenerator.get_date_and_times_in_a_period('1395/03/21 23:00:00' , '1396/03/21 15:00:00'))

########## test and debug code end   ####################
