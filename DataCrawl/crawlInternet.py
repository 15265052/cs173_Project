# 爬取网页中的数据
from bs4 import BeautifulSoup
import requests


def crawler(url):
    # return an crawler
    parser = "lxml"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content.decode('utf-8'), parser)


def have_mainland_diagnosis(report_content: str):
    return report_content.find("新增本") != -1 and report_content.find("新冠肺炎确诊病例") != -1 and report_content.find("无新增本") == -1


def crawl_shanghai():
    # 爬取上海近一年的数据
    # 首先获取所有上海卫健委的疫情通报有本土确诊的病例
    shanghai_mhc_url = "https://wsjkw.sh.gov.cn/xwfb/"
    url_list = []
    page_num = 42
    for i in range(1, page_num):
        if i == 1:
            cur_url = shanghai_mhc_url + "index.html"
        else:
            cur_url = shanghai_mhc_url + "index_" + str(i) + ".html"
        crawl = crawler(cur_url)
        report_list = crawl.select('#main > div.main-container.margin-top-15 > div > ul > li > a')
        for report in report_list:
            report_content = report.text
            if have_mainland_diagnosis(report_content):
                # 内容为疫情通报
                url_list.append((report_content, shanghai_mhc_url + report['href']))
    for content, url in url_list:
        crawl_spec = crawler(url)






crawl_shanghai()
