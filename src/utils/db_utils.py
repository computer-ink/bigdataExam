from pyspark.sql import SparkSession

from src.config.db_config import MYSQL_JDBC_URL, MYSQL_PROPERTIES


def get_mysql_spark_session(app_name="ExtractMySQL"):
    """返回 spark 和 mysql url"""
    spark = SparkSession.builder \
        .appName(app_name) \
        .enableHiveSupport() \
        .getOrCreate()

    return spark, MYSQL_JDBC_URL


def get_db_properties():
    """返回 MySQL 运行配置"""
    return MYSQL_PROPERTIES
