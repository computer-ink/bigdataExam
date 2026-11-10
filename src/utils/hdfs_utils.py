"""HDFS 操作工具：本地文件上传、路径拼接。"""

import os
import subprocess

from src.config.hdfs_config import HDFS_NAMENODE, SOURCE_PATH
from src.config.project_config import CSV_DATA_DIR, CSV_TABLES


def upload_csv_files_to_hdfs():
    """② 上传 data/csv 下的行为流水文件到 HDFS。"""
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", SOURCE_PATH], check=True)
    for table in CSV_TABLES:
        local = os.path.join(CSV_DATA_DIR, f"{table}.csv")
        subprocess.run(
            ["hdfs", "dfs", "-put", "-f", local, f"{SOURCE_PATH}/"],
            check=True,
        )
        print(f"[OK] 上传 {table}.csv -> {SOURCE_PATH}/{table}.csv")


def csv_hdfs_path(table):
    """返回某张 CSV 在 HDFS 上的完整路径。"""
    return f"{HDFS_NAMENODE}{SOURCE_PATH}/{table}.csv"
