# coding = gbk
from common.utils.fileutils import *
import pandas as pd

path = "../DataCrawl/rawdata/all_confirmed_specific_info.json"
store_path = "./processeddata/all_confirmed_specific_data.csv"
raw_data = read_json(path)
patient_pop = ['patient_id', 'sort_time', 'base_info', 'extra_info', 'index']
for info_dict in raw_data:
    info_dict.pop('track_type')
    info_dict.pop('risk_level')
    for patient in info_dict['patient_list']:
        patient['info'] = patient['base_info'] + patient['extra_info']
        for i in patient_pop:
            patient.pop(i)
raw_data = pd.DataFrame(raw_data)
raw_data.to_csv(store_path, index=False)
