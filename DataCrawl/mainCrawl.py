# 综合所有数据源爬取需要的数据
from request import *
from common.utils.fileutils import *

CHINA_CODE = "CHN"
CHINA_NAME = "中国"

all_province_codes = ["AH", "AM", "BJ", "CQ", "FJ", "GD", "GS", "GX", "HB", "HB-1", "HLJ", "HN", "HN-1", "HN-2", "JL"
    , "JL", "JS", "JX", "LN", "NMG", "NX", "QH", "SC", "SD", "SH", "SX", "SX-1", "TJ", "TW", "XG", "XJ"
    , "XZ", "YN", "ZJ"]

data_dir_path = "RawData/"
shanghai_local_id = "310000"


def get_from_apis():
    # # get china daily data
    # china_daily_data = get_one_country_all_daily()['data']['chinaDayList']
    # file_name = "china_daily.json"
    # write_file(data_dir_path + file_name, china_daily_data)
    #
    # china_daily_add_data = get_one_country_add_daily()['data']['chinaDayAddList']
    # file_name = "china_add_daily.json"
    # write_file(data_dir_path + file_name, china_daily_add_data)
    #
    # # get all provinces latest data
    # china_all_provinces_latest_data = get_one_country_one_province_latest()['data']['provinceCompare']
    # file_name = "china_all_provinces_latest_data.json"
    # write_file(data_dir_path + file_name, china_all_provinces_latest_data)

    city_codes = get_all_city_codes()
    all_confirmed_specific_info = []
    # get all shanghai geo tracks data
    for city_code in city_codes:
        all_geo_tracks_data = get_covid_tracks(city_code)

        # get all specific infos of shanghai confirmed
        for di in all_geo_tracks_data['data']['list']:
            if not di['local_id'] == 0:
                try:
                    d = get_covid_confirmed_specific_info(di['poi'])['data']['data']
                    if len(d['patient_list']) != 0:
                        all_confirmed_specific_info.append(d)
                except:
                    continue
            print('finished city: '+city_code)
    file_name = "all_confirmed_specific_info.json"
    write_file(data_dir_path + file_name, all_confirmed_specific_info)


def get_all_city_codes():
    city_codes = []
    raw_list = get_all_city_id()['data']['list']
    for province in raw_list:
        for city in province['city_list']:
            city_codes.append(str(city['city_code']))
    return city_codes


get_from_apis()

