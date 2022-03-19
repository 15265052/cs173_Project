# 综合所有数据源爬取需要的数据
from request import *

CHINA_CODE = "CHN"
CHINA_NAME = "中国"

data_dir_path = "RawData/"


def get_from_apis():
    # get china latest data
    china_latest = get_one_country_latest(CHINA_CODE)
    file_name = "china_latest.json"
    with open(data_dir_path + file_name, "w") as f:
        f.write(str(china_latest))

    # get china daily data
    china_daily_data = get_one_country_all_daily(CHINA_CODE)
    file_name = "china_daily.json"
    with open(data_dir_path + file_name, "w") as f:
        f.write(str(china_daily_data))

    # get news
    china_news = get_covid_related_news(page=1, num=10)
    file_name = "china_news.json"
    with open(data_dir_path+file_name, "w") as f:
        f.write(str(china_news))

    # get all provinces daily data


get_from_apis()
