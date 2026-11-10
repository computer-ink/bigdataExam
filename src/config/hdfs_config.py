"""HDFS / Hive 分布式存储配置。

统一读取 .env 中的 HDFS / Hive 连接信息，并导出数仓
分层落地目录，供 ETL 各阶段读写使用。
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ===== 连接信息 =====
HDFS_NAMENODE = os.getenv("HDFS_NAMENODE", "hdfs://localhost:9000")
HIVE_METASTORE_URIS = os.getenv("HIVE_METASTORE_URIS", "thrift://localhost:9083")

# ===== Hive 库 =====
HIVE_DB = "edu_dw"

# ===== 数仓分层 HDFS 落地目录 =====
HDFS_BASE = "/user/edu_dw"
ODS_PATH = f"{HDFS_BASE}/ods"
DWD_PATH = f"{HDFS_BASE}/dwd"
DIM_PATH = f"{HDFS_BASE}/dim"
DWS_PATH = f"{HDFS_BASE}/dws"
ADS_PATH = f"{HDFS_BASE}/ads"

# ===== Hive 外部表挂载的原始数据目录 =====
SOURCE_PATH = f"{HDFS_BASE}/source"

# 分层目录映射（供脚本遍历使用）
LAYER_PATHS = {
    "ods": ODS_PATH,
    "dwd": DWD_PATH,
    "dim": DIM_PATH,
    "dws": DWS_PATH,
    "ads": ADS_PATH,
}
