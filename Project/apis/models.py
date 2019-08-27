# -*- coding=utf-8 -*-
import os
from django.db import models
from Project import settings
from authorization.models import UserInfo
from utils import id
from datetime import date
from django.utils import timezone


week_choices = (
    (1, '1周'), (2, '2周'), (3, '3周'), (4, '4周'), (5, '5周'),
    (6, '6周'), (7, '7周'), (8, '8周'), (9, '9周'), (10, '10周'),
    (11, '11周'), (12, '12周'), (13, '13周'), (14, '14周'), (15, '15周'),
    (16, '16周'), (17, '17周')
)

day_choices = ((1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'))

class_choices = (
    (1, '1节'), (2, '2节'), (3, '3节'), (4, '4节'), (5, '5节'),
    (6, '6节'), (7, '7节'), (8, '8节'), (9, '9节'), (10, '10节')
)

record_choices = ((0, '缺席'), (1, '请假'), (2, '迟到'), (3, '签到'), (4, '忽略'), (5, '未签到'))


class Activity(models.Model):
    activity_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="活动ID")
    name = models.CharField(max_length=50, null=False, verbose_name="活动名称")
    begin_w = models.IntegerField(null=False, verbose_name="开始周次", choices=week_choices)
    begin_d = models.IntegerField(null=False, verbose_name="开始星期", choices=day_choices)
    begin_c = models.IntegerField(null=False, verbose_name="开始节课", choices=class_choices)
    end_w = models.IntegerField(null=False, verbose_name="结束周次", choices=week_choices)
    end_d = models.IntegerField(null=False, verbose_name="结束星期", choices=day_choices)
    end_c = models.IntegerField(null=False, verbose_name="结束节课", choices=class_choices)
    address = models.CharField(max_length=50, null=False, verbose_name="活动地点")
    clothes = models.BooleanField(default=False, verbose_name="社服要求", choices=((True, '需要'), (False, '不需要')))
    message = models.TextField(null=False, verbose_name="活动流程")
    user = models.ForeignKey(UserInfo, related_name='user', verbose_name="发布者", on_delete=models.SET_NULL, null=True)
    time = models.DateField(default=date.today, verbose_name="发布时间", blank=True)
    status = models.IntegerField(default=1, verbose_name="状态", choices=((2, '进行中'), (1, '未开始'), (0, '已结束')))
    judge_delete = models.BooleanField(default=False, verbose_name="删除判断", choices=((True, '是'), (False, '否')))
    editor = models.ForeignKey(UserInfo, related_name='editor', verbose_name="修改者", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Activity'
        verbose_name = '社团活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)


class Arrange(models.Model):
    arrange_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="人员安排ID")
    activity = models.ForeignKey(Activity, db_column='activity_id', verbose_name="活动", on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, related_name='arrange_user', verbose_name="工作人员", on_delete=models.CASCADE)
    begin_w = models.IntegerField(null=False, verbose_name="开始周次", choices=week_choices)
    begin_d = models.IntegerField(null=False, verbose_name="开始星期", choices=day_choices)
    begin_c = models.IntegerField(null=False, verbose_name="开始节课", choices=class_choices)
    end_w = models.IntegerField(null=False, verbose_name="结束周次", choices=week_choices)
    end_d = models.IntegerField(null=False, verbose_name="结束星期", choices=day_choices)
    end_c = models.IntegerField(null=False, verbose_name="结束节课", choices=class_choices)
    message = models.TextField(null=False, verbose_name="任务说明")
    time = models.DateTimeField(null=True, verbose_name="完成时间", blank=True)
    status = models.BooleanField(default=False, verbose_name="状态", choices=((True, '已完成'), (False, '未完成')))
    editor = models.ForeignKey(UserInfo, related_name='arrange_editor', verbose_name="修改者", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Arrange'
        verbose_name = '工作安排'
        verbose_name_plural = verbose_name


class Material(models.Model):
    material_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="活动物资ID")
    activity = models.ForeignKey(Activity, db_column='activity_id', verbose_name="活动", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, verbose_name="物品名称")
    count = models.IntegerField(default=1, verbose_name="物品数量")
    time = models.DateTimeField(null=True, verbose_name="完成时间", blank=True)
    status = models.BooleanField(default=False, verbose_name="状态", choices=((True, '已完成'), (False, '未完成')))
    editor = models.ForeignKey(UserInfo, related_name='material_editor', verbose_name="修改者", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Material'
        verbose_name = '活动物资'
        verbose_name_plural = verbose_name


class Record(models.Model):
    record_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="签到ID")
    activity = models.ForeignKey(Activity, db_column='activity_id', verbose_name="活动", on_delete=models.CASCADE)
    recorder = models.ForeignKey(UserInfo, related_name='record_recorder', verbose_name="签到员", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserInfo, related_name='record_user', verbose_name="工作人员", on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, verbose_name="签到时间", blank=True)
    status = models.IntegerField(default=5, verbose_name="状态", choices=record_choices)

    class Meta:
        db_table = 'Record'
        verbose_name = '签到'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="评论ID")
    activity = models.ForeignKey(Activity, db_column='activity_id', verbose_name="活动", on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, related_name='comment_user', verbose_name="评论者", on_delete=models.CASCADE)
    message = models.TextField(null=True, verbose_name="内容")
    time = models.DateTimeField(default=timezone.now, verbose_name="评论时间", blank=True)

    class Meta:
        db_table = 'Comment'
        verbose_name = '反思墙'
        verbose_name_plural = verbose_name


class Resource(models.Model):
    resource_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="社团物资ID")
    name = models.CharField(max_length=20, null=False, verbose_name="物品名称")
    count = models.IntegerField(default=1, verbose_name="物品数量")

    class Meta:
        db_table = 'Resource'
        verbose_name = '社团物资'
        verbose_name_plural = verbose_name


class Article(models.Model):
    article_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="文章ID")
    title = models.CharField(max_length=50, null=False, verbose_name="标题")
    message = models.TextField(null=False, verbose_name="内容")
    user = models.ForeignKey(UserInfo, related_name='article_user', verbose_name="发布者", on_delete=models.SET_NULL, null=True)
    time = models.DateField(default=date.today, verbose_name="发布时间", blank=True)
    editor = models.ForeignKey(UserInfo, related_name='article_editor', verbose_name="修改者", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class Image(models.Model):
    image_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="图片ID")
    name = models.CharField(max_length=255, null=False, verbose_name="图片名称")
    user = models.ForeignKey(UserInfo, related_name='image_user', verbose_name="上传者", on_delete=models.SET_NULL, null=True)
    time = models.DateField(default=date.today, verbose_name="上传时间", blank=True)

    class Meta:
        db_table = 'Image'
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def delete(self, *args, **kwargs):
        my_image = os.path.join(settings.IMAGES_DIR, self.name)
        os.remove(my_image)
        super().delete(*args, **kwargs)


class File(models.Model):
    file_id = models.CharField(primary_key=True, max_length=22, default=id.generate_id, verbose_name="文件ID")
    name = models.CharField(max_length=255, null=False, verbose_name="文件名")
    user = models.ForeignKey(UserInfo, related_name='file_user', verbose_name="上传者", on_delete=models.SET_NULL, null=True)
    time = models.DateField(default=date.today, verbose_name="上传时间", blank=True)

    class Meta:
        db_table = 'File'
        verbose_name = '文档'
        verbose_name_plural = verbose_name

    def delete(self, *args, **kwargs):
        my_file = os.path.join(settings.DOCUMENTS_DIR, self.name)
        os.remove(my_file)
        super().delete(*args, **kwargs)

