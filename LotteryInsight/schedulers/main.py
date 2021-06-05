import os
import time
import typing
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def execute_commend(commend_lines: typing.Union[str, typing.List[str]]):
    if isinstance(commend_lines, str):
        logger.info(commend_lines)
        subprocess.call(commend_lines, shell=True)


def execute_daily_cash_crawler():
    commend_line = f"python {PROJECT_PATH}/LotteryInsight/tasks/brain.py --mode=now --table=DailyCash"
    execute_commend(commend_line)


def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="sent DailyCach task",
        func=execute_daily_cash_crawler,
        trigger="cron",
        minute="*/20",
        hour="22-23",
        day_of_week="0-6",
    )
    logger.info("sent DailyCach crawler add scheduler")
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(10)
