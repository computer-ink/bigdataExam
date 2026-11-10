"""项目全局路径与常量。

定义项目根目录、数据目录、SQL 目录等本地路径，
以及文件数据源（行为流水）表清单和数仓分层顺序。
"""

import os

# ===== 项目根目录 =====
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# ===== 本地目录 =====
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MYSQL_DATA_DIR = os.path.join(DATA_DIR, "mysql")   # 静态主数据（导入 MySQL）
CSV_DATA_DIR = os.path.join(DATA_DIR, "csv")       # 行为流水（文件源直接读）
SQL_DIR = os.path.join(PROJECT_ROOT, "sql")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# ===== 文件数据源（行为流水）表清单 =====
CSV_TABLES = [
    "activity_learn_log",            # 学习行为日志
    "log",                           # 操作/登录日志
    "testpaper_result",              # 考试答卷记录
    "user_learn_statistics_total",   # 用户学习统计
]

# ===== 数仓分层顺序（ETL 执行顺序） =====
LAYERS = ["ods", "dwd", "dim", "dws", "ads"]
