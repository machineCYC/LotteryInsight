import typing

import pandas as pd
from loguru import logger
from LotteryInsight import config
from LotteryInsight.tools.datasets import MYSQL_DATABASE_MAPPING
from sqlalchemy import create_engine


def get_mysql_database_conn(database: str = ""):
    address = (
        f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}"
        f"@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{database}"
    )
    mysql_engine = create_engine(address)
    connect = mysql_engine.connect()
    logger.debug(f"get database:{database} connection")
    return connect


def generate_dataframe_insert_update_sql(df: pd.DataFrame, table: str):
    table_columns = list(df.columns)
    list_data = df.values.tolist()
    list_insert_update_commands = []
    for raw in list_data:

        update_sql = ", ".join(
            ["`{0}`='{1}'".format(c, e) for c, e in zip(table_columns, raw)]
        )
        update_sql += ", `SYS_UPDATE_COUNT`=`SYS_UPDATE_COUNT`+1"
        upsert_sql = """INSERT INTO `{0}` ({1}) VALUES ({2}) ON DUPLICATE KEY UPDATE {3}""".format(
            table,
            "`{}`".format("`,`".join(table_columns)),
            "'{}'".format("','".join(raw)),
            update_sql,
        )
        list_insert_update_commands.append(upsert_sql)
    return list_insert_update_commands


def execute_mysql_command(
    sql_command: typing.Union[str, typing.List[str]],
    table: str,
):
    mysql_database = MYSQL_DATABASE_MAPPING.get(table, "")
    mysql_database_conn = get_mysql_database_conn(mysql_database)

    try:
        if isinstance(sql_command, list):
            for s in sql_command:
                logger.debug(f"execute sql:{s}")
                _ = mysql_database_conn.execute(s)
        elif isinstance(sql_command, str):
            logger.debug(f"execute sql:{sql_command}")
            mysql_database_conn.execute(sql_command)
    except Exception as e:
        logger.error(f"mysql_insert: {e}")
        # raise BaseException(f"mysql_insert: {e}")


def query_mysql_command(
    sql_command: typing.Union[str, typing.List[str]],
    table: str,
):
    mysql_database = MYSQL_DATABASE_MAPPING.get(table, "")
    mysql_database_conn = get_mysql_database_conn(mysql_database)

    try:
        logger.debug(f"execute sql:{sql_command}")
        ret = mysql_database_conn.execute(sql_command)
        return ret.fetchall()
    except Exception as e:
        logger.error(f"{e}")
