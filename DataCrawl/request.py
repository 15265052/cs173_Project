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
    url = LEAFCODER_HOST + "/api/" + country_code + "/daily/"
    re = requests.get(url)
    return re.json()


def get_one_country_latest(country_code):
    url = LEAFCODER_HOST + "/api/countries/" + country_code
    re = requests.get(url)
    return re.json()


def get_one_country_all_provinces(country_code):
    url = LEAFCODER_HOST + "/api/provinces/" + country_code + "/daily/"
    re = requests.get(url)
    return re.json()


def get_covid_related_news(page=1, num=10):
    url = ISAACLIN_HOST + "/nCoV/api/news"
    re = requests.get(url)
    return re.json()

