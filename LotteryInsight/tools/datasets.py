dataset_url = {
    "DailyCash": "https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx",  ### 精彩 539
}

MYSQL_DATABASE_MAPPING = {
    "DailyCash": "LotteryData",
}

dataset_column_names = {
    "DailyCash": ["draw_term", "ddate"] + [f"no{i+1}" for i in range(5)],
}
