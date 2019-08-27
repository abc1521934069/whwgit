# -*- encoding=utf8 -*-

from django.db import models
from utils import id
from datetime import date


class College(models.Model):
    college_id = models.IntegerField(primary_key=True, verbose_name="学院ID")
    name = models.CharField(max_length=20, null=False, verbose_name="学院名称")

    class Meta:
        db_table = 'College'
        verbose_name = '学院信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Major(models.Model):
    # 级联删除时置空，需要有null=True
    college = models.ForeignKey(College, db_column='college_id', verbose_name="学院", on_delete=models.SET_NULL, null=True)
    major_id = models.CharField(primary_key=True, max_length=3, verbose_name="专业ID")
    name = models.CharField(max_length=20, null=False, verbose_name="专业名称")

    class Meta:
        db_table = 'Major'
        verbose_name = '专业信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Dept(models.Model):
    dept_id = models.IntegerField(primary_key=True, verbose_name="部门ID")
    name = models.CharField(max_length=20, null=False, verbose_name="部门名称")
    introduce = models.TextField(null=True, verbose_name="部门介绍")
    technology = models.TextField(null=True, verbose_name="职能")
    work = models.TextField(null=True, verbose_name="工作")
    daily = models.TextField(null=True, verbose_name="日常")

    class Meta:
        db_table = 'Dept'
        verbose_name = '部门信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class UserInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="用户ID")
    openid = models.CharField(max_length=50, null=True, verbose_name="微信标识符")
    name = models.CharField(max_length=50, null=True, verbose_name="姓名")
    phone = models.CharField(max_length=11, null=True, verbose_name="手机")
    address = models.CharField(max_length=50, null=True, verbose_name="籍贯")
    birthday = models.DateField(default=date.today, verbose_name="生日", blank=True)
    sex = models.BooleanField(null=True, verbose_name="性别", choices=((True, '男'), (False, '女')))
    college = models.ForeignKey(College, db_column='college_id', verbose_name="学院", on_delete=models.SET_NULL, null=True)
    major = models.ForeignKey(Major, db_column='major_id', verbose_name="专业", on_delete=models.SET_NULL, null=True)
    grade = models.CharField(max_length=2, null=True, verbose_name="年级")
    class_num = models.CharField(max_length=2, null=True, verbose_name="班级")
    dorm = models.CharField(max_length=2, null=True, verbose_name="宿舍")
    dorm_num = models.CharField(max_length=3, null=True, verbose_name="宿舍号")
    introduce = models.TextField(null=True, verbose_name="个人介绍")
    join_time = models.DateField(default=date.today, verbose_name="加入时间", blank=True)
    judge_invalid = models.BooleanField(default=False, verbose_name="账号状态", choices=((True, '有效'), (False, '无效')))

    class Meta:
        db_table = 'UserInfo'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Register(models.Model):
    user = models.OneToOneField(UserInfo, db_column='user_id', verbose_name="用户", on_delete=models.CASCADE)
    # 需要用related_name区分每个字段：
    # ①一个表内2个字段引用于相同的表
    # ②本表外键也引用了本表需要引用的表
    # ③同一个models中，所有引用自同一个表的字段
    dept1 = models.ForeignKey(Dept, related_name='dept1', verbose_name="部门1", on_delete=models.SET_NULL, null=True)
    dept2 = models.ForeignKey(Dept, related_name='dept2', verbose_name="部门2", on_delete=models.SET_NULL, null=True)
    register_time = models.DateField(default=date.today, verbose_name="报名时间", blank=True)

    class Meta:
        db_table = 'Register'
        verbose_name = '报名管理'
        verbose_name_plural = verbose_name


class UserClub(models.Model):
    user = models.OneToOneField(UserInfo, db_column='user_id', verbose_name="用户", on_delete=models.CASCADE)
    dept = models.ForeignKey(Dept, db_column='dept_id', verbose_name="部门", on_delete=models.SET_NULL, null=True)
    position = models.IntegerField(default=0, verbose_name="职位", choices=((0, '干事'), (1, '部长'), (2, '社长')))
    judge_remain = models.BooleanField(default=False, verbose_name="留任", choices=((True, '留任'), (False, '非留任')))

    class Meta:
        db_table = 'UserClub'
        verbose_name = '职位信息'
        verbose_name_plural = verbose_name


class UserPower(models.Model):
    user = models.OneToOneField(UserInfo, db_column='user_id', verbose_name="用户", on_delete=models.CASCADE)
    add_activity = models.BooleanField(default=False, verbose_name="发布活动权限", choices=((True, '有'), (False, '无')))
    edit_activity = models.BooleanField(default=False, verbose_name="修改活动权限", choices=((True, '有'), (False, '无')))
    record = models.BooleanField(default=False, verbose_name="签到权限", choices=((True, '有'), (False, '无')))
    edit_course = models.BooleanField(default=False, verbose_name="修改空课表权限", choices=((True, '有'), (False, '无')))
    add_article = models.BooleanField(default=False, verbose_name="发布文章权限", choices=((True, '有'), (False, '无')))
    edit_article = models.BooleanField(default=False, verbose_name="修改文章权限", choices=((True, '有'), (False, '无')))
    add_image = models.BooleanField(default=False, verbose_name="上传图片权限", choices=((True, '有'), (False, '无')))
    add_file = models.BooleanField(default=False, verbose_name="上传文档权限", choices=((True, '有'), (False, '无')))

    class Meta:
        db_table = 'UserPower'
        verbose_name = '权限管理'
        verbose_name_plural = verbose_name


class UserRecord(models.Model):
    user = models.OneToOneField(UserInfo, db_column='user_id', verbose_name="用户", on_delete=models.CASCADE)
    late = models.IntegerField(default=0, verbose_name="迟到次数")
    request = models.IntegerField(default=0, verbose_name="请假次数")
    absent = models.IntegerField(default=0, verbose_name="缺席次数")
    finish = models.IntegerField(default=0, verbose_name="完成任务次数")
    overtime = models.IntegerField(default=0, verbose_name="超时完成次数")
    incomplete = models.IntegerField(default=0, verbose_name="未完成次数")

    class Meta:
        db_table = 'UserRecord'
        verbose_name = '工作记录'
        verbose_name_plural = verbose_name


class Course(models.Model):
    user = models.OneToOneField(UserInfo, db_column='user_id', verbose_name="用户", on_delete=models.CASCADE)
    course_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="课表ID")
    mon1 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周一1大节")
    mon2 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周一2大节")
    mon3 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周一3大节")
    mon4 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周一4大节")
    mon5 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周一5大节")
    tue1 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周二1大节")
    tue2 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周二2大节")
    tue3 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周二3大节")
    tue4 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周二4大节")
    tue5 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周二5大节")
    wed1 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周三1大节")
    wed2 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周三2大节")
    wed3 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周三3大节")
    wed4 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周三4大节")
    wed5 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周三5大节")
    thu1 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周四1大节")
    thu2 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周四2大节")
    thu3 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周四3大节")
    thu4 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周四4大节")
    thu5 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周四5大节")
    fri1 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周五1大节")
    fri2 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周五2大节")
    fri3 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周五3大节")
    fri4 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周五4大节")
    fri5 = models.CharField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]', max_length=51, null=False, verbose_name="周五5大节")

    class Meta:
        db_table = 'Course'
        verbose_name = '课程表'
        verbose_name_plural = verbose_name

