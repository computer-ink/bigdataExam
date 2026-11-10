"""抽取（Extract）：多源异构数据 → ODS 层。

- 文件数据源（data/csv 下的行为流水 CSV）用 Spark 直接读取
- 业务库源（MySQL 静态主数据）用 Spark JDBC 读取
统一落地为 Hive ODS 层表（edu_dw.ods_<表名>）。

供 etl.run_etl() 调用，不单独运行。
"""

import os

from src.config.db_config import MYSQL_JDBC_URL, MYSQL_PROPERTIES, MYSQL_TABLES
from src.config.hdfs_config import HIVE_DB
from src.config.project_config import CSV_DATA_DIR, CSV_TABLES


def load_csv_to_ods(spark, table):
    """CSV 文件源 → ODS。"""
    path = os.path.join(CSV_DATA_DIR, f"{table}.csv")
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("quote", '"')
        .option("escape", '"')
        # 若 text 字段含换行，追加 .option("multiLine", "true")
        .csv(path)
    )
    df.write.mode("overwrite").saveAsTable(f"{HIVE_DB}.ods_{table}")
    print(f"[OK] CSV {table} -> {HIVE_DB}.ods_{table}  ({df.count()} 行)")


def load_mysql_to_ods(spark, table):
    """MySQL 业务库源 → ODS。"""
    df = spark.read.jdbc(MYSQL_JDBC_URL, table, properties=MYSQL_PROPERTIES)
    df.write.mode("overwrite").saveAsTable(f"{HIVE_DB}.ods_{table}")
    print(f"[OK] MySQL {table} -> {HIVE_DB}.ods_{table}  ({df.count()} 行)")


def run_extract(spark):
    """执行抽取：9 张源表全部落地 ODS 层。"""
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DB}")

    for table in MYSQL_TABLES:
        load_mysql_to_ods(spark, table)

    for table in CSV_TABLES:
        load_csv_to_ods(spark, table)

    print("抽取完成：9 张表全部落地 ODS 层")
