# coding=gbk
from common.utils.fileutils import *
import pandas as pd

path = "../DataCrawl/rawdata/china_all_provinces_daily_data.json"
store_path = "./processeddata/"
file_name = "_province_daily_data.csv"
raw_data = read_json(path)
data_dict = []
for province_list in raw_data:
    for province_daily_list in province_list:
        data_dict.append(province_daily_list)
raw_data = pd.DataFrame(data_dict)
raw_data = raw_data[~raw_data['province'].isin(['香港', '台湾'])]
columns_to_be_deleted = ['confirm_cuts', 'dead_cuts', 'now_confirm_cuts', 'heal_cuts', 'description']
for column in columns_to_be_deleted:
    del raw_data[column]
province_names = raw_data['province'].unique()
for province in province_names:
    temp_data = raw_data[raw_data['province'].isin([province])]
    temp_data.to_csv(store_path+province+file_name, index=False)

