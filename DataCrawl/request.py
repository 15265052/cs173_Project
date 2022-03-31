# request apis
from config.apis import *
import requests


def get_global_latest():
    url = LEAFCODER_HOST + "/api/statistics/latest"
    re = requests.get(url)
    return re.json()


def get_global_all():
    url = LEAFCODER_HOST + "/api/statistics/"
    re = requests.get(url)
    return re.json()


# def get_country_daily(country=None, use_code=False):
#     # default get all country daily data
#     url = LEAFCODER_HOST + "/api/countries/daily/"
#     if country:
#         if use_code:
#             url += "?countryCodes=" + country
#         else:
#             url += "?countryNames=" + country
#
#     re = requests.get(url)
#     return re.json()


def get_one_country_all_daily():
    url = TENCENT_HOST + "query/inner/publish/modules/list?modules=chinaDayList"
    re = requests.get(url)
    return re.json()


def get_one_country_add_daily():
    url = TENCENT_HOST + "query/inner/publish/modules/list?modules=chinaDayAddList"
    re = requests.get(url)
    return re.json()


def get_one_country_all_provinces_daily(country_code):
    url = LEAFCODER_HOST + "/api/provinces/" + country_code + "/daily/"
    re = requests.get(url)
    return re.json()


def get_one_country_one_province_daily(province_name):
    url = TENCENT_HOST + "query/pubished/daily/list?province="+province_name
    re = requests.get(url)
    return re.json()


def get_one_country_one_province_latest():
    url = TENCENT_HOST + "query/inner/publish/modules/list?modules=provinceCompare"
    re = requests.get(url)
    return re.json()


def get_china_one_city_latest(city_name=""):
    url = LEAFCODER_HOST + "/api/cities/CHN/" + city_name
    re = requests.get(url)
    return re.json()


def get_covid_related_news(page=1, num=10):
    url = ISAACLIN_HOST + "/nCoV/api/news?page=" + str(page) + "&num=" + str(num)
    re = requests.get(url)
    return re.json()


def get_covid_tracks(city_code):
    url = TIKTOK_HOST + "track_list/?city_code=" + city_code
    re = requests.get(url)
    return re.json()


def get_covid_confirmed_specific_info(poi):
    try:
        x, y = poi.split(',')
    except:
        return None
    url = TIKTOK_HOST + "poi/?poi=" + x + "%2C" + y
    re = requests.get(url)
    return re.json()


def get_all_city_id():
    url = TIKTOK_HOST + "poi_brief/?start_time=0"
    re = requests.get(url)
    return re.json()

def get_all_china_daily():
    url = "https://file1.dxycdn.com/2022/0330/301/8632025056402530453-135.json?t=27477150"
    return requests.get(url)
