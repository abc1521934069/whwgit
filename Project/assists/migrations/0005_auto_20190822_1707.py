# Generated by Django 2.2.4 on 2019-08-22 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assists', '0004_auto_20190813_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='current_week',
            field=models.IntegerField(choices=[(1, '1周'), (2, '2周'), (3, '3周'), (4, '4周'), (5, '5周'), (6, '6周'), (7, '7周'), (8, '8周'), (9, '9周'), (10, '10周'), (11, '11周'), (12, '12周'), (13, '13周'), (14, '14周'), (15, '15周'), (16, '16周'), (17, '17周')], default=1, verbose_name='当前周次'),
        ),
    ]
