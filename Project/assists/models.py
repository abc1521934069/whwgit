# -*- encoding=utf8 -*-

import os
from django.db import models
from Project import settings


week_choices = (
    (1, '1周'), (2, '2周'), (3, '3周'), (4, '4周'), (5, '5周'),
    (6, '6周'), (7, '7周'), (8, '8周'), (9, '9周'), (10, '10周'),
    (11, '11周'), (12, '12周'), (13, '13周'), (14, '14周'), (15, '15周'),
    (16, '16周'), (17, '17周')
)

class_choices = (
    (1, '1节'), (2, '2节'), (3, '3节'), (4, '4节'), (5, '5节'),
    (6, '6节'), (7, '7节'), (8, '8节'), (9, '9节'), (10, '10节'),
    (11, '晚修结束')
)


class Propagate(models.Model):
    image1 = models.ImageField(upload_to='images', null=True, verbose_name="图片1", blank=True)
    image2 = models.ImageField(upload_to='images', null=True, verbose_name="图片2", blank=True)
    image3 = models.ImageField(upload_to='images', null=True, verbose_name="图片3", blank=True)
    image4 = models.ImageField(upload_to='images', null=True, verbose_name="图片4", blank=True)
    image5 = models.ImageField(upload_to='images', null=True, verbose_name="图片5", blank=True)
    nature = models.TextField(null=False, verbose_name="社团性质")
    activity = models.TextField(null=False, verbose_name="社团活动")

    class Meta:
        db_table = 'Propagate'
        verbose_name = '社团宣传'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        for i in ["1", "2", "3", "4", "5"]:
            try:
                my_image = os.path.join(settings.MEDIA_ROOT, str(self.__dict__["image" + i]))
                os.remove(my_image)
            except:
                pass
        super().save(*args, **kwargs)


class Master(models.Model):
    register = models.BooleanField(default=False, verbose_name="报名管理", choices=((True, '开启'), (False, '关闭')))
    course = models.BooleanField(default=False, verbose_name="空课表编辑", choices=((True, '开启'), (False, '关闭')))
    current_week = models.IntegerField(default=1, verbose_name='当前周次', choices=(
        (1, '1周'), (2, '2周'), (3, '3周'), (4, '4周'), (5, '5周'), (6, '6周'), (7, '7周'),
        (8, '8周'), (9, '9周'), (10, '10周'), (11, '11周'), (12, '12周'), (13, '13周'), (14, '14周'),
        (15, '15周'), (16, '16周'), (17, '17周')
    ))

    class Meta:
        db_table = 'Master'
        verbose_name = '特权'
        verbose_name_plural = verbose_name


class TimeMapping(models.Model):
    class_num = models.IntegerField(null=False, verbose_name="节课", choices=class_choices)
    time = models.DateTimeField(null=False, verbose_name="上课时间", blank=True)

    class Meta:
        db_table = 'TimeMapping'
        verbose_name = '课程时间映射'
        verbose_name_plural = verbose_name

