# Generated by Django 2.2.4 on 2019-08-23 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assists', '0005_auto_20190822_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timemapping',
            name='time',
            field=models.DateTimeField(blank=True, verbose_name='上课时间'),
        ),
    ]