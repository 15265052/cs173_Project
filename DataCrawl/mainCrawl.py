# 综合所有数据源爬取需要的数据
from request import *
import common

from common.utils.fileutils import *

CHINA_CODE = "CHN"
CHINA_NAME = "中国"

all_province_codes = ["AH", "AM", "BJ", "CQ", "FJ", "GD", "GS", "GX", "HB", "HB-1", "HLJ", "HN", "HN-1", "HN-2", "JL"
    , "JL", "JS", "JX", "LN", "NMG", "NX", "QH", "SC", "SD", "SH", "SX", "SX-1", "TJ", "TW", "XG", "XJ"
    , "XZ", "YN", "ZJ"]

data_dir_path = "RawData/"
shanghai_local_id = "310000"
city_dict = {"shanghai": "310000", "changchun": "220100", "xiameng": "350200", "tianjin": "120000", "qingdao": "370200"}


def get_from_apis():
    # get china daily data
    china_daily_data = get_one_country_all_daily()['data']['chinaDayList']
    file_name = "china_daily.json"
    write_file(data_dir_path + file_name, china_daily_data)

    china_daily_add_data = get_one_country_add_daily()['data']['chinaDayAddList']
    file_name = "china_add_daily.json"
    write_file(data_dir_path + file_name, china_daily_add_data)

    # get all provinces latest data
    china_all_provinces_latest_data = get_one_country_one_province_latest()['data']['provinceCompare']
    file_name = "china_all_provinces_latest_data.json"
    write_file(data_dir_path + file_name, china_all_provinces_latest_data)

    # get all shanghai geo tracks data
    for city in city_dict.keys():
        all_geo_tracks_data = get_covid_tracks(city_dict[city])
        file_name = city + "_all_ego_tracks_data.json"
        write_file(data_dir_path + file_name, all_geo_tracks_data)

        # get all specific infos of shanghai confirmed
        all_confirmed_specific_info = []
        for di in all_geo_tracks_data['data']['list']:
            if not di['local_id'] == 0:
                for track in di['tracks']:
                    all_confirmed_specific_info.append(get_covid_confirmed_specific_info(track['poi']))
        file_name = city + "_all_confirmed_specific_info.json"
        write_file(data_dir_path + file_name, all_confirmed_specific_info)


get_from_apis()
