import argparse
import importlib
from loguru import logger

from LotteryInsight.tools import db
from LotteryInsight.tools.datasets import MYSQL_DATABASE_MAPPING


def main(args):
    if args.mode != "now":
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

    logger.info(f"start praser table:{args.table} data with mode:{args.mode}")
    if args.mode == "now":
        df = getattr(
            importlib.import_module(f"LotteryInsight.crawlers.{args.table}"),
            "update_new",
        )()
    elif args.mode == "history":
        df = getattr(
            importlib.import_module(f"LotteryInsight.crawlers.{args.table}"),
            "update_history",
        )()
    elif args.mode == "period":
        pass
    else:
        df = pd.DataFrame([])
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
        "--mode",
        help="Example: now means crawler today data.",
        default="history",
        choices=["now", "history", "period"],
        type=str,
    )
    parser.add_argument(
        "--table",
        help="Example: DailyCash means process this dataset",
        default="Lotto649",
        choices=["DailyCash", "Lotto649"],
        type=str,
    )
    args = parser.parse_args()

    main(args)
