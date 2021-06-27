import re
import time
from datetime import date

import pandas as pd
import requests
from loguru import logger

from LotteryInsight.tools.datasets import dataset_url, dataset_column_names
from LotteryInsight.utility.common import get_header, get_validation_information
from LotteryInsight.utility.date import (
    get_today,
    split_date2yearmonthdate,
    transfer_commonera2rocera,
    create_year_month_list,
    get_ym,
)


TABLE = "Lotto649"
url = dataset_url.get(TABLE, "")
column_names = dataset_column_names.get(TABLE, "")


def create_table_sql():
    sql = f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                draw_term VARCHAR(9) NOT NULL,
                ddate DATE NOT NULL,
                no1 INT NOT NULL,
                no2 INT NOT NULL,
                no3 INT NOT NULL,
                no4 INT NOT NULL,
                no5 INT NOT NULL,
                no6 INT NOT NULL,
                sno INT NOT NULL,
                SYS_CREATE_TIME DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                SYS_UPDATE_TIME DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                SYS_UPDATE_COUNT INT NOT NULL DEFAULT 0,
                PRIMARY KEY (draw_term, ddate)
            );
            """
    return sql


def clean_string_date(date: str):
    y, m, d = date.split("-")
    return "-".join([str(int(y) + 1911), m, d])


def get_html(url, year, month):
    headers = get_header()
    validaiton_info_dict = get_validation_information(url, headers)

    post_data = {
        "__VIEWSTATE": validaiton_info_dict.get("__VIEWSTATE"),
        "__VIEWSTATEGENERATOR": validaiton_info_dict.get(
            "__VIEWSTATEGENERATOR"
        ),
        "__EVENTVALIDATION": validaiton_info_dict.get("__EVENTVALIDATION"),
        "Lotto649Control_history$txtNO": "",
        "Lotto649Control_history$chk": "radYM",
        "Lotto649Control_history$dropYear": year,
        "Lotto649Control_history$dropMonth": month,
        "Lotto649Control_history$btnSubmit": "查詢",
    }
    res = requests.post(url=url, data=post_data, headers=headers)

    string_html = res.text
    return string_html


def parser_win_ball_number(html, is_today):
    # 期別
    draw_term_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_L649_DrawTerm_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_L649_DrawTerm_\d{1,2}">(.*?)</span>'
    )
    draw_terms = re.findall(draw_term_pattern, html)

    # 開獎日期
    ddate_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_L649_DDate_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_L649_DDate_\d{1,2}">(.*?)</span>'
    )
    ddates = re.findall(ddate_pattern, html)
    ddates = [clean_string_date(d.replace("/", "-")) for d in ddates]

    # 開出順序
    no1_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_SNo1_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_SNo1_\d{1,2}">(.*?)</span>'
    )
    on1s = re.findall(no1_pattern, html)

    no2_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_SNo2_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_SNo2_\d{1,2}">(.*?)</span>'
    )
    on2s = re.findall(no2_pattern, html)

    no3_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_SNo3_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_SNo3_\d{1,2}">(.*?)</span>'
    )
    on3s = re.findall(no3_pattern, html)

    no4_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_SNo4_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_SNo4_\d{1,2}">(.*?)</span>'
    )
    on4s = re.findall(no4_pattern, html)

    no5_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_SNo5_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_SNo5_\d{1,2}">(.*?)</span>'
    )
    on5s = re.findall(no5_pattern, html)

    no6_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_SNo6_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_SNo6_\d{1,2}">(.*?)</span>'
    )
    on6s = re.findall(no6_pattern, html)

    sno7_pattern = (
        r'<span id="Lotto649Control_history_dlQuery_No7_0">(.*?)</span>'
        if is_today
        else r'<span id="Lotto649Control_history_dlQuery_No7_\d{1,2}">(.*?)</span>'
    )
    son7 = re.findall(sno7_pattern, html)
    data = []
    for dt, dd, o1, o2, o3, o4, o5, o6, so7 in zip(
        draw_terms, ddates, on1s, on2s, on3s, on4s, on5s, on6s, son7
    ):
        data.append([str(dt), dd, o1, o2, o3, o4, o5, o6, so7])

    time.sleep(3)
    return data


def update_new():
    today = get_today()
    logger.info(f"update {TABLE} {today} data")

    year, month, day = split_date2yearmonthdate(today)
    roc_year = transfer_commonera2rocera(year)

    html = get_html(url, int(roc_year), int(month))
    data = parser_win_ball_number(html, True)

    datas = pd.DataFrame(data, columns=column_names)
    datas = datas[datas["ddate"] == today]
    return datas


def update_history():  # TODO: add interval update
    logger.info(f"start update {TABLE} history data")
    ym = get_ym()

    # start 103 year
    ym_list = create_year_month_list(start_ym="2014-01", end_ym=ym)

    datas = []
    for d in ym_list:
        year = d.get("year")
        roc_year = transfer_commonera2rocera(year)
        month = d.get("month")

        html = get_html(url, int(roc_year), month)
        data = parser_win_ball_number(html, False)
        logger.info(f"update {TABLE} history {d} data, count:{len(data)}")
        datas.extend(data)

    datas = pd.DataFrame(datas, columns=column_names)
    datas = datas.sort_values(by=["draw_term", "ddate"])
    return datas