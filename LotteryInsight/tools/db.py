import pandas as pd
from LotteryInsight.tools.datasets import MYSQL_DATABASE_MAPPING
from sqlalchemy import create_engine
from LotteryInsight import config


def get_mysql_database_conn(database: str=''):
    address = (
        f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}"
        f"@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{database}"
    )
    mysql_engine = create_engine(address)
    connect = mysql_engine.connect()
    return connect


def update_mysql_data(df: pd.DataFrame, table: str):
    mysql_database = MYSQL_DATABASE_MAPPING.get(table, "")
    mysql_database_conn = get_mysql_database_conn(mysql_database)

    try:
        df.to_sql(name=table, con=mysql_database_conn, index=False, if_exists="append")
    except Exception as e:
        raise BaseException(f"mysql_insert: {e}")
