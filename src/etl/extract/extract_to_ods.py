"""抽取（Extract）：多源异构数据 → ODS 层。

- CSV 文件源：先上传 HDFS（流程 ②），再用 Spark 从 HDFS 读取
- 业务库源（MySQL 静态主数据）用 Spark JDBC 读取
统一落地为 Hive ODS 外部表（edu_dw.ods_<表名>，数据在 /user/edu_dw/ods）。

供 etl.run_etl() 调用，不单独运行。
"""

from src.config.db_config import MYSQL_JDBC_URL, MYSQL_PROPERTIES, MYSQL_TABLES
from src.config.hdfs_config import HIVE_DB
from src.config.project_config import CSV_TABLES
from src.utils.hdfs_utils import csv_hdfs_path, upload_csv_files_to_hdfs
from src.utils.spark_utils import save_to_layer


def load_csv_to_ods(spark, table):
    """CSV 文件源（HDFS）→ ODS。"""
    path = csv_hdfs_path(table)
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("quote", '"')
        .option("escape", '"')
        # 若 text 字段含换行，追加 .option("multiLine", "true")
        .csv(path)
    )
    save_to_layer(spark, df, "ods", f"ods_{table}")
    print(f"[OK] CSV {table} -> {HIVE_DB}.ods_{table}  ({df.count()} 行)")


def load_mysql_to_ods(spark, table):
    """MySQL 业务库源 → ODS。"""
    df = spark.read.jdbc(MYSQL_JDBC_URL, table, properties=MYSQL_PROPERTIES)
    save_to_layer(spark, df, "ods", f"ods_{table}")
    print(f"[OK] MySQL {table} -> {HIVE_DB}.ods_{table}  ({df.count()} 行)")


def run_extract(spark):
    """执行抽取：9 张源表全部落地 ODS 层。"""
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DB}")

    # 上传 CSV 行为流水到 HDFS
    upload_csv_files_to_hdfs()

    for table in MYSQL_TABLES:
        load_mysql_to_ods(spark, table)

    for table in CSV_TABLES:
        load_csv_to_ods(spark, table)

    print("抽取完成：9 张表全部落地 ODS 层")
