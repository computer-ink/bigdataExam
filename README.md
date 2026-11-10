# 教育数据仓库系统

《基于 Hadoop 的教育数据仓库系统的设计与实现》——在线教育平台多源异构数据接入 → ETL → 分层数仓建模（星型 + 雪花模型）。

## 技术栈
- 数据源：MySQL（业务库）+ CSV（埋点/行为日志文件）
- 计算引擎：PySpark（Spark SQL / DataFrame）
- 存储：HDFS + Hive（Metastore）
- 分层：ODS → DWD → DIM → DWS → ADS

## 整体流程（Hadoop 使用位置）

Hadoop 从「抽取」开始贯穿整个数仓：HDFS 存储 + Hive 元数据/SQL + Spark 分布式计算。

```
┌─────────────────────────────────────────────────────────────┐
│                     数据源层（多源异构）                      │
├───────────────────────────────┬─────────────────────────────┤
│  MySQL 业务库（静态主数据 5 张） │  CSV 文件（行为流水 4 张）   │
│  ① pandas 导入 MySQL ── 非 Hadoop │  ② 上传 HDFS             │
└───────────────┬───────────────┴──────────────┬──────────────┘
                │ ③ Spark JDBC 抽取            │ ③ Spark read csv
                ▼                              ▼
   ╔═══════════════════════════════════════════════════════╗
   ║        Hadoop 集群（HDFS + Hive Metastore + Spark）    ║
   ╚═══════════════════════════════════════════════════════╝
                │
                ▼
   ③ ODS 层（Hive 表 → 落在 HDFS）
                │ ④ Spark 清洗转换
                ▼
   ④ DWD 层（Hive 表 → HDFS）
                │ ⑤ Spark 维度/事实建模
                ▼
   ⑤ DIM 维度表 + FACT 事实表（Hive → HDFS）
                │ ⑥ Spark 聚合
                ▼
   ⑥ DWS 汇总层（Hive → HDFS）
                │
                ▼
   ⑦ ADS 应用层（Hive → HDFS）
                │ ⑧ Hive / Spark SQL 查询
                ▼
   ⑧ 报表 / 可视化 / 现场演示
```

## 目录结构
```
bigdataExam/
├── data/
│   ├── mysql/                    # 静态主数据（导入 MySQL 业务库，5 张）
│   └── csv/                      # 行为流水文件源（直接读取，4 张）
├── docs/                         # 项目文档（说明文档、字段说明、PPT）
├── sql/                          # 全部 SQL 脚本
│   ├── mysql/                    # 业务库（源库）建表 DDL
│   ├── ods/                      # ODS 层：原始数据接入（落地 Hive 外部表）
│   ├── dwd/                      # DWD 层：明细层（清洗、去重、格式统一）
│   ├── dim/                      # DIM 层：维度表（代理键 + 雪花挂靠）
│   ├── dws/                      # DWS 层：汇总层（轻度聚合）
│   └── ads/                      # ADS 层：应用层（报表口径）
├── src/                          # Python 代码
│   ├── config/                   # 配置（MySQL/HDFS/项目常量）
│   ├── utils/                    # 公共工具（Spark/HDFS/日志）
│   ├── etl/
│   │   ├── extract/              # 抽取：CSV / MySQL → ODS
│   │   ├── transform/            # 清洗转换：ODS → DWD / DIM
│   │   └── load/                 # 加载：DWD/DIM → DWS / ADS
│   ├── dim/                      # 维度建模逻辑（DimUser/Course/Chapter/Task/Test/Time）
│   ├── fact/                     # 事实表建模逻辑（FactLearning/FactTestResults/…）
│   └── jobs/                     # 编排入口（一键跑全流程）
├── scripts/                      # 环境初始化、一键运行、演示脚本
├── output/                       # 运行产物（报表结果、截图）
├── .env                          # 连接配置（MySQL / Hive / HDFS）
└── README.md
```

## 数据存放策略（多源异构）

> 静态维度数据 → MySQL；行为流水数据 → CSV 文件；最终全部 ETL 进 Hadoop 建数仓。

| 存储位置 | 数据性质 | 表 |
|----------|----------|----|
| **MySQL（业务库源）** | 静态主数据（维度来源） | course_chapter、course_task、classroom_member、classroom_courses、testpaper |
| **CSV 文件（文件源）** | 时序行为流水（事实来源） | activity_learn_log、log、testpaper_result、user_learn_statistics_total |
| **Hadoop（Hive/HDFS）** | 数仓最终存储 | 以上全部 ETL 后按 ODS/DWD/DIM/DWS/ADS 分层落地 |

- ODS 层：MySQL 用 Spark JDBC 抽取；CSV 用 `spark.read.csv` 读入 HDFS
- DWD/DIM/DWS/ADS：清洗、建模、汇总统一在 Hive 完成

## 源表 → 数仓映射（概览）
| 源表 | 说明 | 数仓归属 |
|------|------|----------|
| course_chapter | 课程章节 | DimChapter（雪花挂 DimCourse） |
| course_task | 课程任务 | DimTask（雪花挂 DimChapter） |
| classroom_member / classroom_courses | 班级成员/课程 | DimUser / DimCourse |
| testpaper / testpaper_result | 试卷/答卷 | DimTest + FactTestResults |
| activity_learn_log / log | 行为/日志流水 | FactLearning |
| user_learn_statistics_total | 学习统计 | DWS 汇总 |

## 快速开始
1. `bash scripts/init_env.sh` —— 初始化 HDFS 目录、Hive 库
2. `bash scripts/run_etl.sh` —— 一键执行 ETL 全流程
3. 查询 `ads` 层表产出报表口径结果
