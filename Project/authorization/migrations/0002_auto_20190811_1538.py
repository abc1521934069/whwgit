# Generated by Django 2.2.3 on 2019-08-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='openid',
            field=models.CharField(max_length=50, null=True, verbose_name='微信标识符'),
        ),
    ]
