"""将 data/mysql 下的静态主数据 CSV 写入 MySQL 业务库。

小文件，使用 pandas + sqlalchemy（pymysql 驱动）。
流程：先执行 create_tables.sql 建库建表，再运行本脚本加载数据。

运行：python sql/mysql/load_to_mysql.py
"""

import os
import sys

# 保证从任意目录运行都能导入 src 包
sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)

import pandas as pd
from sqlalchemy import create_engine, text

from src.config.db_config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DB,
    MYSQL_TABLES,
)
from src.config.project_config import MYSQL_DATA_DIR


def get_engine():
    """创建 SQLAlchemy 引擎（pymysql 驱动）。"""
    url = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    return create_engine(url)


def truncate_table(engine, table):
    """清空表，保证可重复执行。"""
    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE `{table}`"))
        conn.commit()


def load_csv_to_mysql(engine, table):
    """读取单个 CSV 并写入对应 MySQL 表。"""
    csv_path = os.path.join(MYSQL_DATA_DIR, f"{table}.csv")
    df = pd.read_csv(csv_path)
    truncate_table(engine, table)
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"[OK] {table}: {len(df)} 行 -> MySQL")


def main():
    engine = get_engine()
    for table in MYSQL_TABLES:
        load_csv_to_mysql(engine, table)
    engine.dispose()
    print("全部业务表写入 MySQL 完成")


if __name__ == "__main__":
    main()
