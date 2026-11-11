"""SparkSession 统一入口 + 分层写入工具。"""

from pyspark.sql import SparkSession

from src.config.hdfs_config import HIVE_DB, HDFS_NAMENODE, LAYER_PATHS


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


def save_to_layer(spark, df, layer, table):
    """写 DataFrame 到 HDFS 分层目录，并注册为 Hive 外部表。

    layer: ods / dwd / dim / dws / ads
    table: 完整表名（含层前缀），如 ods_course_chapter
    数据落点：LAYER_PATHS[layer]/table（如 /user/edu_dw/ods/ods_course_chapter）
    """
    location = f"{HDFS_NAMENODE}{LAYER_PATHS[layer]}/{table}"
    df.write.mode("overwrite").format("orc").save(location)
    spark.sql(
        f"CREATE EXTERNAL TABLE IF NOT EXISTS {HIVE_DB}.{table} "
        f"USING ORC LOCATION '{location}'"
    )
