-- =============================================================
-- 教育数据仓库 —— MySQL 业务库（静态主数据源）建表脚本
-- 说明：先运行本脚本建库建表，再运行 load_to_mysql.py 加载 CSV 数据
-- 执行：mysql -uroot -p < create_tables.sql
-- =============================================================

CREATE DATABASE IF NOT EXISTS edu_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE edu_db;

-- -------------------------------------------------------------
-- 1. 课程章节表 course_chapter
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS course_chapter (
    `id`                    INT UNSIGNED NOT NULL COMMENT '课程章节ID',
    `courseId`              INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '章节所属课程ID',
    `type`                  VARCHAR(255) DEFAULT NULL COMMENT '章节类型：chapter/unit/lesson',
    `number`                INT UNSIGNED DEFAULT 0 COMMENT '章节编号',
    `seq`                   INT UNSIGNED DEFAULT 0 COMMENT '章节序号',
    `title`                 VARCHAR(255) DEFAULT NULL COMMENT '章节名称',
    `createdTime`           INT UNSIGNED DEFAULT 0 COMMENT '章节创建时间',
    `updatedTime`           INT UNSIGNED DEFAULT 0 COMMENT '修改时间',
    `copyId`                INT DEFAULT 0 COMMENT '复制章节的ID',
    `status`                VARCHAR(20) DEFAULT NULL COMMENT '发布状态',
    `isOptional`            TINYINT(1) DEFAULT 0 COMMENT '是否选修',
    `migrateLessonId`       INT DEFAULT 0 COMMENT '迁移课时ID',
    `migrateCopyCourseId`   INT DEFAULT 0 COMMENT '迁移复制课程ID',
    `migrateRefTaskId`      INT DEFAULT 0 COMMENT '迁移参考任务ID',
    `mgrateCopyTaskId`      INT DEFAULT 0 COMMENT '迁移复制任务ID',
    `migrate_task_id`       INT NOT NULL DEFAULT 0 COMMENT '来源任务表ID',
    `published_number`      INT UNSIGNED DEFAULT 0 COMMENT '已发布的章节编号',
    PRIMARY KEY (`id`),
    KEY `idx_courseId` (`courseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程章节表';

-- -------------------------------------------------------------
-- 2. 课程任务表 course_task
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS course_task (
    `id`                INT UNSIGNED NOT NULL COMMENT '主键',
    `courseId`          INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '所属课程ID',
    `fromCourseSetId`   INT UNSIGNED DEFAULT 0 COMMENT '课程集合引用ID',
    `seq`               INT UNSIGNED DEFAULT 1 COMMENT '序号',
    `categoryId`        INT DEFAULT NULL COMMENT '类别ID',
    `activityId`        INT UNSIGNED DEFAULT 0 COMMENT '教学活动ID',
    `title`             VARCHAR(255) DEFAULT NULL COMMENT '标题',
    `isFree`            INT UNSIGNED DEFAULT 0 COMMENT '是否免费',
    `isOptional`        INT UNSIGNED DEFAULT 0 COMMENT '是否必修',
    `startTime`         INT UNSIGNED DEFAULT 0 COMMENT '开始时间',
    `endTime`           INT UNSIGNED DEFAULT 0 COMMENT '结束时间',
    `status`            VARCHAR(255) DEFAULT 'create' COMMENT '发布状态',
    `createdUserId`     INT UNSIGNED DEFAULT 0 COMMENT '创建者ID',
    `createdTime`       INT UNSIGNED DEFAULT 0 COMMENT '创建时间',
    `updatedTime`       INT UNSIGNED DEFAULT 0 COMMENT '最后更新时间',
    `mode`              VARCHAR(60) DEFAULT NULL COMMENT '任务模式',
    `isLesson`          TINYINT(1) DEFAULT 0 COMMENT '是否固定课时',
    `number`            VARCHAR(32) DEFAULT '' COMMENT '任务编号',
    `type`              VARCHAR(50) DEFAULT NULL COMMENT '任务类型',
    `mediaSource`       VARCHAR(32) DEFAULT '' COMMENT '媒体文件来源',
    `length`            INT UNSIGNED DEFAULT 0 COMMENT '时长或页数',
    `maxOnlineNum`      INT UNSIGNED DEFAULT 0 COMMENT '最大同时在线人数，0不限制',
    `copyId`            INT DEFAULT 0 COMMENT '复制来源task的ID',
    `migrateLessonId`   INT DEFAULT 0 COMMENT '迁移课时ID',
    PRIMARY KEY (`id`),
    KEY `idx_courseId` (`courseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程任务表';

-- -------------------------------------------------------------
-- 3. 班级成员表 classroom_member
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS classroom_member (
    `id`                INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
    `classroomId`       INT UNSIGNED DEFAULT 0 COMMENT '班级ID',
    `userId`            INT UNSIGNED DEFAULT 0 COMMENT '用户ID',
    `orderId`           INT UNSIGNED DEFAULT 0 COMMENT '订单ID',
    `levelId`           INT UNSIGNED DEFAULT 0 COMMENT '等级',
    `noteNum`           INT UNSIGNED DEFAULT 0 COMMENT '笔记数',
    `threadNum`         INT UNSIGNED DEFAULT 0 COMMENT '话题数',
    `locked`            TINYINT UNSIGNED DEFAULT 0 COMMENT '是否锁定',
    `role`              VARCHAR(255) DEFAULT 'auditor' COMMENT '角色',
    `createdTime`       INT UNSIGNED DEFAULT 0 COMMENT '创建时间',
    `lastLearnTime`     INT DEFAULT NULL COMMENT '最后学习时间',
    `learnedNum`        INT DEFAULT NULL COMMENT '已学课时数',
    `updatedTime`       INT DEFAULT 0 COMMENT '最后更新时间',
    `deadline`          INT UNSIGNED DEFAULT 0 COMMENT '到期时间',
    `refundDeadline`    INT DEFAULT 0 COMMENT '退款截止日期',
    `deadlineNotified`  INT DEFAULT 0 COMMENT '有效期通知',
    PRIMARY KEY (`id`),
    KEY `idx_classroomId` (`classroomId`),
    KEY `idx_userId` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班级成员表';

-- -------------------------------------------------------------
-- 4. 班级课程表 classroom_courses
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS classroom_courses (
    `id`                INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
    `classroomId`       INT UNSIGNED DEFAULT 0 COMMENT '班级ID',
    `courseId`          INT UNSIGNED DEFAULT 0 COMMENT '课程ID',
    `parentCourseId`    INT UNSIGNED DEFAULT 0 COMMENT '父课程ID',
    `seq`               INT UNSIGNED DEFAULT 0 COMMENT '班级课程顺序',
    `disabled`          TINYINT UNSIGNED DEFAULT 0 COMMENT '是否禁用',
    `courseSetId`       INT DEFAULT 0 COMMENT '课程集合ID',
    PRIMARY KEY (`id`),
    KEY `idx_classroomId` (`classroomId`),
    KEY `idx_courseId` (`courseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班级课程表';

-- -------------------------------------------------------------
-- 5. 试卷信息表 testpaper
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS testpaper (
    `id`                INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name`              VARCHAR(255) DEFAULT NULL COMMENT '试卷名称',
    `courseId`          INT DEFAULT NULL COMMENT '课程ID',
    `lessonId`          INT DEFAULT NULL COMMENT '课时ID',
    `limitedTime`       INT UNSIGNED DEFAULT 0 COMMENT '限时(秒)',
    `pattern`           VARCHAR(255) DEFAULT NULL COMMENT '试卷生成/显示模式',
    `target`            VARCHAR(255) DEFAULT NULL COMMENT '目标',
    `status`            VARCHAR(32) DEFAULT 'draft' COMMENT '试卷状态',
    `score`             FLOAT(10,1) UNSIGNED DEFAULT 0.0 COMMENT '总分',
    `passedCondition`   TEXT COMMENT '通过条件',
    `itemCount`         INT UNSIGNED DEFAULT 0 COMMENT '题目数量',
    `questionTypeSeq`   VARCHAR(64) DEFAULT NULL COMMENT '题型排序',
    `createdTime`       INT UNSIGNED DEFAULT 0 COMMENT '创建时间',
    `updatedTime`       INT UNSIGNED DEFAULT 0 COMMENT '修改时间',
    `metas`             TEXT COMMENT '题型排序等附属信息',
    `type`              VARCHAR(32) DEFAULT NULL COMMENT '测验类型',
    `courseSetId`       INT UNSIGNED DEFAULT 0 COMMENT '课程集合ID',
    PRIMARY KEY (`id`),
    KEY `idx_courseId` (`courseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='试卷信息表';
