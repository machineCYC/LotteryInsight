import re
import os
import time
import csv
from datetime import date
from typing import List

import pandas as pd
import requests
from loguru import logger

from LotteryInsight.tools.datasets import dataset_url
from LotteryInsight.utility.common import download_csv


url = dataset_url.get("DailyCash", "")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
}


def get_validation_information(url, headers):
    # 創建網路連接
    s = requests.Session()

    # 獲取網頁查詢資訊"認證"
    r = s.get(url=url, headers=headers)
    __VIEWSTATEGENERATORpat = re.compile(
        '<input.*?id="__VIEWSTATEGENERATOR" value="(.*?)" />'
    )
    __VIEWSTATEGENERATOR = __VIEWSTATEGENERATORpat.findall(r.text)[0]
    __VIEWSTATEpat = re.compile('<input.*?id="__VIEWSTATE" value="(.*?)" />')
    __VIEWSTATE = __VIEWSTATEpat.findall(r.text)[0]
    __EVENTVALIDATIONpat = re.compile(
        '<input.*?id="__EVENTVALIDATION" value="(.*?)" />'
    )
    __EVENTVALIDATION = __EVENTVALIDATIONpat.findall(r.text)[0]

    validaiton_info_dict = {
        "__VIEWSTATE": __VIEWSTATE,
        "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
        "__EVENTVALIDATION": __EVENTVALIDATION,
    }
    return validaiton_info_dict


def get_html(url, year, month):
    validaiton_info_dict = get_validation_information(url, headers)
    request = requests.post(url=url)

    post_data = {
        "__VIEWSTATE": validaiton_info_dict.get("__VIEWSTATE"),
        "__VIEWSTATEGENERATOR": validaiton_info_dict.get(
            "__VIEWSTATEGENERATOR"
        ),
        "__EVENTVALIDATION": validaiton_info_dict.get("__EVENTVALIDATION"),
        "D539Control_history1$chk": "radYM",
        "D539Control_history1$dropYear": year,
        "D539Control_history1$dropMonth": month,
        "D539Control_history1$btnSubmit": "查詢",
    }

    res = requests.post(url=url, data=post_data)

    string_html = res.text
    return string_html


def parser_win_ball_number(html):
    # 期別
    draw_term_pattern = r'<span id="D539Control_history1_dlQuery_D539_DrawTerm_\d{1,2}">(.*?)</span>'
    draw_terms = re.findall(draw_term_pattern, html)

    # 開獎日期
    ddate_pattern = r'<span id="D539Control_history1_dlQuery_D539_DDate_\d{1,2}">(.*?)</span>'
    ddates = re.findall(ddate_pattern, html)

    # 開出順序
    no1_pattern = (
        r'<span id="D539Control_history1_dlQuery_SNo1_\d{1,2}">(.*?)</span>'
    )
    on1s = re.findall(no1_pattern, html)

    no2_pattern = (
        r'<span id="D539Control_history1_dlQuery_SNo2_\d{1,2}">(.*?)</span>'
    )
    on2s = re.findall(no2_pattern, html)

    no3_pattern = (
        r'<span id="D539Control_history1_dlQuery_SNo3_\d{1,2}">(.*?)</span>'
    )
    on3s = re.findall(no3_pattern, html)

    no4_pattern = (
        r'<span id="D539Control_history1_dlQuery_SNo4_\d{1,2}">(.*?)</span>'
    )
    on4s = re.findall(no4_pattern, html)

    no5_pattern = (
        r'<span id="D539Control_history1_dlQuery_SNo5_\d{1,2}">(.*?)</span>'
    )
    on5s = re.findall(no5_pattern, html)

    data = []
    for dt, dd, o1, o2, o3, o4, o5 in zip(
        draw_terms, ddates, on1s, on2s, on3s, on4s, on5s
    ):
        data.append([dt, dd, o1, o2, o3, o4, o5])

    return data


def update_new():
    # TODO: update current day
    pass


def update_history(update2db: bool = False):  # TODO: add interval update
    today = date.today().strftime("%Y-%m-%d")

    start_year = 103

    end_year, end_month = today.split("-")[:2]
    end_year = int(end_year) - 1911
    end_month = int(end_month)

    years = [y for y in range(start_year, end_year + 1, 1)]
    months = [m for m in range(1, 13)]
    ym_list = [
        dict(year=y, month=m)
        for y in years
        for m in months
        if not ((y == end_year) and (m > end_month))
    ]

    column_names = ["draw_term", "ddate"] + [f"no{i+1}" for i in range(5)]
    datas = []
    for d in ym_list:
        logger.info(d)
        year = d.get("year")
        month = d.get("month")

        html = get_html(url, year, month)
        data = parser_win_ball_number(html)
        time.sleep(3)

        if update2db:
            # TODO: update to db
            pass
        else:
            filepath = "./LotteryInsight/data/DailyCash.csv"
            _ = download_csv(data, filepath, column_names)

        datas.extend(data)

    datas = pd.DataFrame(datas, columns=column_names)
    datas = datas.sort_values(by=["draw_term", "ddate"])
    return datas


_ = update_history()

print("gg")
