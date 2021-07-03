from LotteryInsight.crawlers.DailyCash import update


def test_update():
    df = update(start_date='2021-07-02', end_date='2021-07-02')
    assert len(df) > 0