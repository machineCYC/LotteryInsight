import argparse
import importlib
from loguru import logger

from LotteryInsight.tools import db
from LotteryInsight.tools.datasets import MYSQL_DATABASE_MAPPING


def main(args):
    if args.create_table == "True":
        logger.info(f"check table:{args.table} database exist or not")
        database = MYSQL_DATABASE_MAPPING.get(args.table, "")
        conn = db.get_mysql_database_conn()
        sql = f"CREATE DATABASE IF NOT EXISTS {database};"
        conn.execute(sql)
        conn.close()

        logger.info(f"check table:{args.table} exist or not")
        conn = db.get_mysql_database_conn(database=database)
        sql = getattr(
            importlib.import_module(f"LotteryInsight.crawlers.{args.table}"),
            "create_table_sql",
        )()
        conn.execute(sql)
        conn.close()

    logger.info(
        f"start praser table:{args.table} data, from {args.start_date} to {args.end_date}"
    )
    df = getattr(
        importlib.import_module(f"LotteryInsight.crawlers.{args.table}"),
        "update",
    )(args.start_date, args.end_date)
    logger.info(f"get {len(df)} data")

    if len(df) > 0:
        logger.info(f"insert data to mysql table:{args.table}")
        # df = check_schema(df.copy(), table)
        sql_command = db.generate_dataframe_insert_update_sql(
            df=df, table=args.table
        )
        db.execute_mysql_command(sql_command=sql_command, table=args.table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send crawler to paser data.")
    parser.add_argument(
        "--create_table",
        help="Decide to create table or not. if true, create or replace table else not.",
        default="False",
        type=str,
    )
    parser.add_argument(
        "--start_date",
        help="Crawler data start date.",
        default="2014-01-01",
        type=str,
    )
    parser.add_argument(
        "--end_date",
        help="Crawler data end date",
        default="2021-07-03",
        type=str,
    )
    parser.add_argument(
        "--table",
        help="Example: DailyCash means process this dataset",
        default="Superlotto638",
        choices=["DailyCash", "Lotto649", "Superlotto638"],
        type=str,
    )
    args = parser.parse_args()

    main(args)
