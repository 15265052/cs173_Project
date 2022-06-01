# 综合所有数据源爬取需要的数据
from request import *
import common

from common.utils.fileutils import *
from concurrent.futures import ThreadPoolExecutor
import threading
from multiprocessing import Queue
import time

CHINA_CODE = "CHN"
CHINA_NAME = "中国"

data_dir_path = "RawData/"
shanghai_local_id = "310000"
queue = []


def get_from_apis():
    # get china daily data
    # china_daily_data = get_all_china_daily()
    # file_name = "china_daily_data.json"
    # open(data_dir_path + file_name, 'wb').write(china_daily_data.content)
    #
    # # # get all provinces latest data
    # china_all_provinces_daily_data = request_all_provinces_daily(get_all_province_names())
    # file_name = "china_all_provinces_daily_data.json"
    # write_file(data_dir_path + file_name, china_all_provinces_daily_data)

    request_all_confirmed_specific_info(get_all_city_codes())
    file_name = "all_confirmed_specific_info.json"
    write_file(data_dir_path + file_name, queue)


def get_all_city_codes():
    city_codes = []
    raw_list = get_all_city_id()['data']['list']
    for province in raw_list:
        for city in province['city_list']:
            city_codes.append(str(city['city_code']))
    return city_codes


def request_all_confirmed_specific_info(city_codes):
    pool = ThreadPoolExecutor(max_workers=8)
    global task_sum
    task_sum = 0

    def add_to_queue(future):
        # callback
        global task_sum
        task_sum -= 1
        print("done a task, now task sum: " + str(task_sum))
        if future.result() is None:
            return
        d = future.result()[0]['data']['data']
        d['time'] = future.result()[1]
        if len(d['patient_list']) != 0:
            queue.append(d)
            print('now num of results: ' + str(len(queue)))

    for city_code in city_codes:
        print("dealing with city: " + city_code)
        all_geo_tracks_data = get_covid_tracks(city_code)
        for di in all_geo_tracks_data['data']['list']:
            if not (di['local_id'] == 0 or di['poi'] == ""):
                try:
                    task_sum += 1
                    dt = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(di['poi_time']))
                    future = pool.submit(get_covid_confirmed_specific_info, di['poi'], dt)
                    future.add_done_callback(add_to_queue)
                except:
                    continue
        time.sleep(0.1)
        print("task sum: " + str(task_sum))
    pool.shutdown(wait=True)


def request_all_provinces_daily(province_names):
    province_data = []
    for province_name in province_names:
        print("dealing with name: " + province_name)
        province_data.append(get_one_country_one_province_daily(province_name)['data'])
    return province_data



def get_all_province_names():
    province_dict = get_one_country_one_province_latest()
    return province_dict['data']['provinceCompare'].keys()


get_from_apis()
