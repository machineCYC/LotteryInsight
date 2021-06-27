dataset_url = {
    "DailyCash": "https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx",  ### 精彩 539
    "Lotto649": "https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx",  ### 大樂透
}

MYSQL_DATABASE_MAPPING = {
    "DailyCash": "LotteryData",
    "Lotto649": "LotteryData",
}

dataset_column_names = {
    "DailyCash": ["draw_term", "ddate"] + [f"no{i+1}" for i in range(5)],
    "Lotto649": ["draw_term", "ddate"]
    + [f"no{i+1}" for i in range(6)]
    + ["sno"],
}
