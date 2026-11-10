"""ETL 总编排：按阶段调用抽取、清洗转换等模块。
"""

from src.utils.spark_utils import get_spark_session
from src.etl.extract.extract_to_ods import run_extract
from src.etl.transform.clean_dwd import run_transform


def run_etl():
    """执行完整 ETL 流程：抽取 -> 清洗转换。"""
    spark = get_spark_session("EDU_DW_ETL")
    try:
        run_extract(spark)
        run_transform(spark)
    finally:
        spark.stop()
