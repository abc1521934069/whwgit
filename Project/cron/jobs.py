# -*- coding=utf-8 -*-

import os
from assists.models import Master
from django.db.models import F
from datetime import datetime


def AutoAddCurrentWeek():
    Master.objects.update(current_week=F("current_week") + 1)
    return


def BackUp():
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    os.system("mysqldump --opt -h 127.0.0.1 -u root -proot --lock-all-tables whw>/home/whw/" + now + ".sql")
    return
