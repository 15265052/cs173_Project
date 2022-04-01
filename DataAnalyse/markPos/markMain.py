# coding=gbk
import json
from common.utils.fileutils import *
from DataAnalyse.config.constants import *
from DataAnalyse.config.amapApi import *
import requests
from concurrent.futures import ThreadPoolExecutor

data_path = "../../DataClean/processeddata/all_confirmed_specific_data.csv"

def searchPoiCate(text, city=None):
    url = AMAP_HOST + "/place/text?keywords="+text
    if not city is None:
        url += "&city="+city
    url += "&key="+AMAP_KEY
    data = requests.get(url).json()
    if data['count'] != 0:
        return data['pois'][0]['type']
    else:
        return '其他'
global types
types = []
def add_to_type(future):
    global types
    types.append(future.result())
data = read_csv(data_path)
pool = ThreadPoolExecutor(max_workers=8)
for _, row in data.iterrows():
    city = row['city']
    place_name = row['area_name'] + row['township'] + row['poi_name']
    print("搜索"+place_name)
    future = pool.submit(searchPoiCate, place_name, city)
    future.add_done_callback(add_to_type)
pool.shutdown(wait=True)
data.insert(loc=6, column='place_type', value=types)
del data['patient_list']
data.to_csv("data/marked_specific_info.csv")
