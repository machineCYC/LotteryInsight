import os
import time
import typing
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from LotteryInsight.utility.date import get_today


PROJECT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def execute_commend(commend_lines: typing.Union[str, typing.List[str]]):
    if isinstance(commend_lines, str):
        logger.info(commend_lines)
        subprocess.call(commend_lines, shell=True)


def execute_daily_cash_crawler():
    today = get_today()
    commend_line = f"python {PROJECT_PATH}/LotteryInsight/tasks/brain.py \
        --create_table=False \
        --start_date={today} \
        --end_date={today} \
        --table=DailyCash"
    execute_commend(commend_line)


def execute_lotto649_crawler():
    today = get_today()
    commend_line = f"python {PROJECT_PATH}/LotteryInsight/tasks/brain.py \
        --create_table=False \
        --start_date={today} \
        --end_date={today} \
        --table=Lotto649"
    execute_commend(commend_line)


def execute_superlotto638_crawler():
    today = get_today()
    commend_line = f"python {PROJECT_PATH}/LotteryInsight/tasks/brain.py \
        --create_table=False \
        --start_date={today} \
        --end_date={today} \
        --table=Superlotto638"
    execute_commend(commend_line)


def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="sent DailyCach task",
        func=execute_daily_cash_crawler,
        trigger="cron",
        minute="*/15",
        hour="22-22",
        day_of_week="0-6",
    )
    logger.info("sent DailyCach crawler add scheduler")
    scheduler.add_job(
        id="sent Lotto649 task",
        func=execute_lotto649_crawler,
        trigger="cron",
        minute="*/20",
        hour="22-22",
        day_of_week="2-5",
    )
    logger.info("sent Lotto649 crawler add scheduler")
    scheduler.add_job(
        id="sent Superlotto638 task",
        func=execute_superlotto638_crawler,
        trigger="cron",
        minute="*/20",
        hour="22-22",
        day_of_week="1-4",
    )
    logger.info("sent Superlotto638 crawler add scheduler")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(10)
