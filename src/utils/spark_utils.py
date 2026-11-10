"""SparkSession 统一入口。"""

from pyspark.sql import SparkSession


def get_spark_session(app_name="EDU_DW"):
    """返回开启 Hive 支持的 SparkSession。"""
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .enableHiveSupport()
        .getOrCreate()
    )
