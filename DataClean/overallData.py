# cleaning overall data
import json

import pandas as pd
path = "../DataCrawl/rawdata/china_daily.json"
store_path = "C:/Users/duxiaoyuan/Desktop/OnWorking/CS131/Project/DataClean/processeddata/overall.csv"
with open(path, "r") as f:
    data = json.loads(f.read().replace("\'", "\""))
raw_data = pd.DataFrame(data)
columns_to_be_deleted = ['importedCase', 'heal', 'localConfirmH5', 'noInfectH5', 'healRate', 'deadRate', 'dead',
                         'suspect', 'nowSevere', 'local_acc_confirm']
for column in columns_to_be_deleted:
    del raw_data[column]
raw_data['date'] = raw_data['y'] + '.' + raw_data['date']
del raw_data['y']

