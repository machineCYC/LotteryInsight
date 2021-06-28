import os
import re
import csv
import typing
import requests

from loguru import logger


def clean_string_date(date: str):
    y, m, d = date.split("-")
    return "-".join([str(int(y) + 1911), m, d])


def get_header():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    }
    return headers


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


def download_csv(data: typing.List, filepath: str, column_names: typing.List):
    row_count = len(data)
    is_file_exit = os.path.isfile(filepath)
    mode = "a" if is_file_exit else "w"
    with open(filepath, mode, newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not is_file_exit:
            writer.writerow(column_names)
        process_percentage = [int(i * 0.1 * row_count) for i in range(0, 10)]
        for idx, row in enumerate(data):
            writer.writerow(row)
            if idx in process_percentage:
                logger.debug(
                    f"{process_percentage.index(idx) * 10} % ({idx}/{row_count}) has already processed"
                )
