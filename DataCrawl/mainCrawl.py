# 综合所有数据源爬取需要的数据
from request import *
from common.utils.fileutils import *

CHINA_CODE = "CHN"
CHINA_NAME = "中国"

all_province_codes = ["AH", "AM", "BJ", "CQ", "FJ", "GD", "GS", "GX", "HB", "HB-1", "HLJ", "HN", "HN-1", "HN-2", "JL"
                      , "JL", "JS", "JX", "LN", "NMG", "NX", "QH", "SC", "SD", "SH", "SX", "SX-1", "TJ", "TW", "XG", "XJ"
                      , "XZ", "YN", "ZJ"]

data_dir_path = "RawData/"


def get_from_apis():
    # get china latest data
    china_latest = get_one_country_latest(CHINA_CODE)
    file_name = "china_latest.json"
    write_file(data_dir_path+file_name, china_latest)

    # get china daily data
    china_daily_data = get_one_country_all_daily(CHINA_CODE)
    file_name = "china_daily.json"
    write_file(data_dir_path+file_name, china_daily_data)

    # get news
    china_news = get_covid_related_news(page=1, num=10)
    file_name = "china_news.json"
    write_file(data_dir_path+file_name, china_news)

    # get all provinces daily data
    china_all_provinces_daily_data = get_one_country_all_provinces_daily(CHINA_CODE)
    file_name = "china_all_provinces_daily_data.json"
    write_file(data_dir_path+file_name, china_all_provinces_daily_data)

    # get all provinces latest data
    china_all_provinces_latest_data = get_one_country_one_province_latest(CHINA_CODE)
    file_name = "china_all_provinces_latest_data.json"
    write_file(data_dir_path+file_name, china_all_provinces_latest_data)

    # get all cities latest data
    china_all_cities_latest_data = get_china_one_city_latest()
    file_name = "china_all_cities_latest_data.json"
    write_file(data_dir_path + file_name, china_all_cities_latest_data)


get_from_apis()
