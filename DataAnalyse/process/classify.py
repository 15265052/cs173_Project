# coding=gbk
from datetime import datetime
import spark
from common.utils.fileutils import *
file_path = './data/processed_data.json'
with open(file_path, "r", encoding='gbk') as f:
    data = json.loads(f.read())
processed_data = dict()
for one_data in data:
    one_data['time'] = one_data['time'].split(' ')[0]
    one_data['true_city'] = one_data['city'].split('市')[0] + '市'
    if not processed_data.__contains__(one_data['true_city']):
        processed_data[one_data['true_city']] = []
    processed_data[one_data['true_city']].append(one_data)

for city in processed_data.keys():
    processed_data[city] = sorted(processed_data[city], key=lambda x: datetime.strptime(x['time'], "%Y:%m:%d")
                                     .timestamp())
classify_dict = {'0': {}, '1': {}, '2': {}, '3': {}}
for city in processed_data.keys():
    for item in processed_data[city]:
        try:
            classify_dict[item['cluster']][city].append(item)
        except:
            classify_dict[item['cluster']][city] = []
for i in classify_dict.keys():
    store_path = './data/classified_data_' + i + '.json'
    write_file(store_path, classify_dict[i])

