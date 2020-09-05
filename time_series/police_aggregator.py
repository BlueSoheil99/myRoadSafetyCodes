import pandas as pd
import os
import lxml

'''
this code merges all crashes of country into one single excel file
+
renames province names into English
'''

output_name = 'merge_whole_police.xlsx'
_dir = r'D:\Educational\proje\data\police'  # root directory
input_directory = 'train data'
# input directory should contain ONLY one-year police excel source_dataframes in ONE specific format.
output_directory = 'extracted data'


os.chdir(_dir)
source_dataframes = [pd.read_excel(input_directory + '\\' + i) for i in os.listdir(input_directory)]
english_dict = {'آ غ': 'Azarbayjan_w', 'آ ش': 'Azarbayjan_e', 'آذربايجان شرقي': 'Azarbayjan_e',
                'آذربايجان غربي': 'Azarbayjan_w', 'اصفهان': 'Esfahan', 'ايلام': 'Ilam', 'اردبيل': 'Ardebil',
                'بوشهر': 'Bushehr', 'تهران': 'Tehran', 'تهران شرق': 'Tehran', 'تهران غرب': 'Tehran', 'البرز': 'Alborz',
                'چ و ب': 'Charmahal', 'چهارمحال و بختياري': 'Charmahal', 'خ جنوبي': 'Khoarsan_s',
                'خ رضوي': 'Khoarsan_r', 'خ شمالي': 'Khoarsan_n', 'خراسان': 'Khoarsan_r', 'خراسان ج': 'Khoarsan_s',
                'خراسان ش': 'Khoarsan_n', 'خراسان رضوي': 'Khoarsan_r', 'خراسان شمالي': 'Khoarsan_n',
                'خراسان جنوبي': 'Khoarsan_s', 'خوزستان': 'Khouzestan', 'زنجان': 'Zanjan', 'س و ب': 'Sistan',
                'س و ب ج': 'Sistan', 'سيستان و بلوچستان': 'Sistan', 'سيستان و بلوچستان ج': 'Sistan', 'سمنان': 'Semnan',
                'فارس': 'Fars', 'فارس ج': 'Fars', 'قزوين': 'Qazvin', 'قم': 'Qom', 'كردستان': 'Kordestan',
                'كرمان': 'Kerman', 'كرمان ج': 'Kerman', 'كرمانشاه': 'Kermanshah', 'ك و ب': 'Kohgiluyeh',
                'كهگيلويه و بويراحمد': 'Kohgiluyeh', 'گلستان': 'Golestan', 'گيلان': 'Gilan', 'لرستان': 'Lorestan',
                'مازندران': 'Mazandaran', 'مركزي': 'Markazi', 'هرمزگان': 'Hormozgan', 'همدان': 'Hamedan', 'يزد': 'Yazd'}

for dataframe in source_dataframes:
    for index, row in dataframe.iterrows():
        ostan = row['استان']
        print(index)  # log
        print(ostan)  # log
        if type(ostan) != str:
            dataframe.drop([index])
            continue
        dataframe.at[index, 'استان'] = english_dict[ostan]

        print(row['استان'])    # log # hmmm the row won't change but dataframe actually changes so we are fine!
        print("--- --- --- ---")  # log


data = pd.concat(source_dataframes)
del row, index, dataframe
source_dataframes.clear()
data.reset_index(drop=True, inplace=True)

data.to_excel(output_directory + '\\' + output_name, index=False)
