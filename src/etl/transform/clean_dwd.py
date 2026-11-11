"""清洗转换（Transform）：ODS 层 → DWD 明细层。

对每张 ODS 表做通用清洗：
1. 过滤主键 id 为空的脏数据
2. 按主键 id 去重
3. 时间戳（unix 秒）统一转换为标准 datetime 字符串（*_dt 列）

统一落地为 Hive DWD 外部表（edu_dw.dwd_<表名>，数据在 /user/edu_dw/dwd）。
供 etl.run_etl() 调用，不单独运行。
"""

from pyspark.sql.functions import col, from_unixtime, when

from src.config.db_config import MYSQL_TABLES
from src.config.hdfs_config import HIVE_DB
from src.config.project_config import CSV_TABLES
from src.utils.spark_utils import save_to_layer

# 每张表需要转换为标准时间的时间戳字段
TIMESTAMP_COLS = {
    "course_chapter": ["createdTime", "updatedTime"],
    "course_task": ["startTime", "endTime", "createdTime", "updatedTime"],
    "classroom_member": ["createdTime", "lastLearnTime", "updatedTime"],
    "classroom_courses": [],
    "testpaper": ["createdTime", "updatedTime"],
    "log": ["createdTime"],
    "user_learn_statistics_total": ["createdTime", "updatedTime"],
    "activity_learn_log": ["createdTime"],
    "testpaper_result": ["beginTime", "endTime", "updateTime", "checkedTime"],
}

ALL_TABLES = MYSQL_TABLES + CSV_TABLES


def to_datetime(col_name):
    """时间戳 > 0 才转换，否则置空（清洗脏数据）。"""
    return when(
        col(col_name).isNotNull() & (col(col_name) > 0),
        from_unixtime(col(col_name).cast("long"), "yyyy-MM-dd HH:mm:ss"),
    )


def transform_table(spark, table):
    """单表清洗：ODS -> DWD。"""
    df = spark.table(f"{HIVE_DB}.ods_{table}")

    # 去空：主键为空的脏数据剔除
    df = df.filter(col("id").isNotNull())
    # 去重：按主键去重
    df = df.dropDuplicates(["id"])
    # 时间格式统一：追加 *_dt 标准时间列
    for ts in TIMESTAMP_COLS.get(table, []):
        if ts in df.columns:
            df = df.withColumn(f"{ts}_dt", to_datetime(ts))

    save_to_layer(spark, df, "dwd", f"dwd_{table}")
    print(f"[OK] {HIVE_DB}.ods_{table} -> {HIVE_DB}.dwd_{table}  ({df.count()} 行)")


def run_transform(spark):
    """执行清洗转换：ODS -> DWD 全表处理。"""
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {HIVE_DB}")

    for table in ALL_TABLES:
        transform_table(spark, table)

    print("清洗转换完成：ODS -> DWD 全表处理完毕")
