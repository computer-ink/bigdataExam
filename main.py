"""主程序入口：一键执行完整数据仓库构建流程。

流程：
  1. load_mysql()  静态主数据导入 MySQL（pandas，非 Hadoop）
  2. run_etl()     上传 CSV 到 HDFS + 抽取 ODS + 清洗 DWD（Spark/Hadoop）
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.etl.etl import run_etl
from src.utils.mysql_utils import load_mysql


def main():
    # 静态主数据导入 MySQL 业务库
    load_mysql()
    # 上传 HDFS + 抽取 ODS + 清洗 DWD
    run_etl()


if __name__ == "__main__":
    main()
