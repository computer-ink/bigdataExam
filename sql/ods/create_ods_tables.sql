-- =============================================================
-- ODS 层建表脚本（参考用）
-- 说明：extract_to_ods.py 使用 saveAsTable 会自动按 Spark 推断
--       schema 建表；本脚本为 ODS 层目标 schema 的参考 DDL。
-- =============================================================

CREATE DATABASE IF NOT EXISTS edu_dw;

-- -------------------------------------------------------------
-- 业务库源（MySQL 静态主数据，5 张）
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS edu_dw.ods_course_chapter (
    id                    INT,
    courseId              INT,
    type                  STRING,
    number                INT,
    seq                   INT,
    title                 STRING,
    createdTime           BIGINT,
    updatedTime           BIGINT,
    copyId                INT,
    status                STRING,
    isOptional            TINYINT,
    migrateLessonId       INT,
    migrateCopyCourseId   INT,
    migrateRefTaskId      INT,
    mgrateCopyTaskId      INT,
    migrate_task_id       INT,
    published_number      INT
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_course_task (
    id                INT,
    courseId          INT,
    fromCourseSetId   INT,
    seq               INT,
    categoryId        INT,
    activityId        INT,
    title             STRING,
    isFree            INT,
    isOptional        INT,
    startTime         BIGINT,
    endTime           BIGINT,
    status            STRING,
    createdUserId     INT,
    createdTime       BIGINT,
    updatedTime       BIGINT,
    mode              STRING,
    isLesson          TINYINT,
    number            STRING,
    type              STRING,
    mediaSource       STRING,
    length            INT,
    maxOnlineNum      INT,
    copyId            INT,
    migrateLessonId   INT
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_classroom_member (
    id                INT,
    classroomId       INT,
    userId            INT,
    orderId           INT,
    levelId           INT,
    noteNum           INT,
    threadNum         INT,
    locked            TINYINT,
    role              STRING,
    createdTime       BIGINT,
    lastLearnTime     BIGINT,
    learnedNum        INT,
    updatedTime       BIGINT,
    deadline          BIGINT,
    refundDeadline    BIGINT,
    deadlineNotified  INT
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_classroom_courses (
    id                INT,
    classroomId       INT,
    courseId          INT,
    parentCourseId    INT,
    seq               INT,
    disabled          TINYINT,
    courseSetId       INT
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_testpaper (
    id                INT,
    name              STRING,
    courseId          INT,
    lessonId          INT,
    limitedTime       INT,
    pattern           STRING,
    target            STRING,
    status            STRING,
    score             FLOAT,
    passedCondition   STRING,
    itemCount         INT,
    questionTypeSeq   STRING,
    createdTime       BIGINT,
    updatedTime       BIGINT,
    metas             STRING,
    type              STRING,
    courseSetId       INT
)
STORED AS ORC;

-- -------------------------------------------------------------
-- 文件数据源（行为流水 CSV，4 张）
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS edu_dw.ods_log (
    id                INT,
    userId            INT,
    module            STRING,
    action            STRING,
    data              STRING,
    browser           STRING,
    operatingSystem   STRING,
    device            STRING,
    createdTime       BIGINT,
    level             STRING
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_user_learn_statistics_total (
    id                  INT,
    userId              INT,
    joinedClassroomNum  INT,
    joinedCourseSetNum  INT,
    joinedCourseNum     INT,
    exitClassroomNum    INT,
    exitCourseSetNum    INT,
    exitCourseNum       INT,
    learnedSeconds      BIGINT,
    finishedTaskNum     INT,
    createdTime         BIGINT,
    updatedTime         BIGINT
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_activity_learn_log (
    id            INT,
    activityId    INT,
    courseTaskId  INT,
    userId        INT,
    mediaType     STRING,
    event         STRING,
    data          STRING,
    learnedTime   INT,
    createdTime   BIGINT
)
STORED AS ORC;

CREATE TABLE IF NOT EXISTS edu_dw.ods_testpaper_result (
    id               INT,
    paperName        STRING,
    testId           INT,
    userId           INT,
    courseId         INT,
    lessonId         INT,
    score            FLOAT,
    objectiveScore   FLOAT,
    subjectiveScore  FLOAT,
    teacherSay       STRING,
    rightItemCount   INT,
    passedStatus     STRING,
    limitedTime      INT,
    beginTime        BIGINT,
    endTime          BIGINT,
    updateTime       BIGINT,
    metas            STRING,
    status           STRING,
    checkTeacherId   INT,
    checkedTime      BIGINT,
    usedTime         INT,
    type             STRING,
    courseSetId      INT
)
STORED AS ORC;
