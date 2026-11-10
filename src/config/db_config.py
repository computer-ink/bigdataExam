"""MySQL 业务库连接配置（静态主数据源）。

统一读取 .env 中的 MySQL 连接信息，并导出 JDBC 连接串、
连接属性以及需要导入 MySQL 的业务表清单。
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ===== 连接信息 =====
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "edu_db")

# JDBC 连接串
MYSQL_JDBC_URL = (
    f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    "?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8"
)

# Spark JDBC 连接属性
MYSQL_PROPERTIES = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "driver": "com.mysql.cj.jdbc.Driver",
}

# ===== 业务表清单（静态主数据，导入 MySQL 业务库） =====
MYSQL_TABLES = [
    "course_chapter",      # 课程章节
    "course_task",         # 课程任务
    "classroom_member",    # 班级成员
    "classroom_courses",   # 班级课程
    "testpaper",           # 试卷信息
]
