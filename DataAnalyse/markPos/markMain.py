# coding=gbk
import json
from common.utils.fileutils import *
from DataAnalyse.config.constants import *
from DataAnalyse.config.amapApi import *
import requests
from concurrent.futures import ThreadPoolExecutor

data_path = "../../DataClean/processeddata/all_confirmed_specific_data.csv"


def searchPoiCate(index, text, city=None):
    url = AMAP_HOST + "/place/text?keywords=" + text
    if not city is None:
        url += "&city=" + city
    url += "&key=" + AMAP_KEY_JCH
    try:
        d = requests.get(url).json()
        ret = (index, d['pois'][0]['type'])
    except:
        print(1)
        ret = (index, '待定')
    return ret


global types
types = []
patient_info = []


def add_to_type(future):
    global types
    types.append(future.result())


data = read_csv(data_path)
length = len(data)
start = 45000
end = length
data = data[start:end]

pool = ThreadPoolExecutor(max_workers=8)
for i in data.index:
    city = data['city'][i]
    place_name = data['area_name'][i] + data['township'][i] + data['poi_name'][i]
    place_name = place_name.replace("?", "")
    future = pool.submit(searchPoiCate, i, place_name, city)
    future.add_done_callback(add_to_type)
    p = json.loads(data['patient_list'][i].replace("\"", "").replace("\'", "\""))
    patient_info.append(p[0]['info'])
pool.shutdown(wait=True)
types = sorted(types, key=lambda x: x[0])
types = [t[1] for t in types]

data.insert(loc=6, column='place_type', value=types)
data.insert(loc=7, column='patient_info', value=patient_info)
del data['patient_list']
data.to_csv("data/marked_specific_info_"+str(start) + "_" + str(end) + ".csv")
