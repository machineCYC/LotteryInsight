from LotteryInsight.crawlers.Superlotto638 import update


def test_update():
    df = update(start_date='2021-07-08', end_date='2021-07-08')
    assert len(df) > 0