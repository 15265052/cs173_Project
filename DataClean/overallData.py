# cleaning overall data
import json

import pandas as pd

path = "../DataCrawl/rawdata/china_daily.json"
store_path = "./processeddata/overall.csv"
with open(path, "r") as f:
    data = json.loads(f.read().replace("\'", "\""))
raw_data = pd.DataFrame(data)
columns_to_be_deleted = ['importedCase', 'heal', 'localConfirmH5', 'noInfectH5', 'healRate', 'deadRate', 'dead',
                         'suspect', 'nowSevere', 'local_acc_confirm']
for column in columns_to_be_deleted:
    del raw_data[column]
raw_data['date'] = raw_data['y'] + '.' + raw_data['date']
del raw_data['y']

path = "../DataCrawl/rawdata/china_add_daily.json"
with open(path, "r") as f:
    data = json.loads(f.read().replace("\'", "\""))
raw_add_data = pd.DataFrame(data)
columns_to_be_deleted = ['deadRate', 'healRate', 'importedCase', 'dead', 'heal', 'suspect', 'localinfectionadd']
for column in columns_to_be_deleted:
    del raw_add_data[column]
del raw_add_data['y'], raw_add_data['date']
raw_add_data.rename(columns={'confirm': 'confirmadd', 'infect': 'noInfectadd'}, inplace=True)
overall_data = pd.concat([raw_data, raw_add_data], axis=1)
column_order = ["date", "localConfirm", "confirm", "nowConfirm", "noInfect", "localConfirmadd", "noInfectadd",
                 "confirmadd"]
overall_data = overall_data[column_order]
overall_data.to_csv(store_path)
