# -*- encoding=utf8 -*-

# 直接运行文件与数据库进行交互时，需要加上以下4行代码配置
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project.settings")
django.setup()
