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


def get_country_daily(country=None, use_code=False):
    # default get all country daily data
    url = LEAFCODER_HOST + "/api/countries/daily/"
    if country:
        if use_code:
            url += "?countryCodes=" + country
        else:
            url += "?countryNames=" + country

    re = requests.get(url)
    return re.json()


def get_one_country_all_daily(country_code):
    url = LEAFCODER_HOST + "/api/countries/" + country_code + "/daily/"
    re = requests.get(url)
    return re.json()


def get_one_country_latest(country_code):
    url = LEAFCODER_HOST + "/api/countries/" + country_code
    re = requests.get(url)
    return re.json()


def get_one_country_all_provinces_daily(country_code):
    url = LEAFCODER_HOST + "/api/provinces/" + country_code + "/daily/"
    re = requests.get(url)
    return re.json()


def get_one_country_one_province_daily(country_code, province_code):
    url = LEAFCODER_HOST + "/api/provinces/" + country_code + "/" + province_code + "/daily/"
    re = requests.get(url)
    return re.json()


def get_one_country_one_province_latest(country_code, province_code=""):
    url = LEAFCODER_HOST + "/api/provinces/" + country_code + "/" + province_code
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


def get_covid_tracks(local_id):
    url = TIKTOK_HOST + "district_stat/?local_id=" + local_id
    re = requests.get(url)
    return re.json()


def get_covid_confirmed_specific_info(poi):
    x, y = poi.split(',')
    url = TIKTOK_HOST + "poi/?poi=" + x +"%2C" + y
    re = requests.get(url)
    return re.json()
