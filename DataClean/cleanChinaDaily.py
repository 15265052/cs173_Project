# cleaning overall data
from common.utils.fileutils import *
import pandas as pd

path = "../DataCrawl/rawdata/china_daily_data.json"
store_path = "./processeddata/china_daily.csv"
raw_data = pd.DataFrame(read_json(path)['data'])
columns_to_be_deleted = ['highDangerCount', 'midDangerCount', 'suspectedCount', 'suspectedCountIncr']
for column in columns_to_be_deleted:
    del raw_data[column]
raw_data.to_csv(store_path)
