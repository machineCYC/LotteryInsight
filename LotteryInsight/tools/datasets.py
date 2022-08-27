dataset_url = {
    "DailyCash": "https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx",  ### 精彩 539
    "Lotto649": "https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx",  ### 大樂透
    "Superlotto638": "https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx",  ### 威力彩
}

MYSQL_DATABASE_MAPPING = {
    "DailyCash": "LotteryData",
    "Lotto649": "LotteryData",
    "Superlotto638": "LotteryData",
}

dataset_column_names = {
    "DailyCash": ["draw_term", "ddate"] + [f"no{i+1}" for i in range(5)],
    "Lotto649": ["draw_term", "ddate"]
    + [f"no{i+1}" for i in range(6)]
    + ["sno"],
    "Superlotto638": ["draw_term", "ddate"]
    + [f"no{i+1}" for i in range(6)]
    + ["sno"],
}
