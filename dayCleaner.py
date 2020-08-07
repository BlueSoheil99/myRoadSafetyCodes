import pandas as pd


def clean_dataset(dataframe):
    for index, row in dataframe.iterrows():
        if row['total observed'] != row['total estimated']:
            row['total estimated'] = get_an_estimation(row)
    return dataframe


def get_an_estimation(row):
    # todo make currenct estimations
    # if row['interval'] != 60:
    return round(row['total observed'] * 60 / row['interval'])



