# -*- encoding=utf8 -*-
import xadmin
from .models import Propagate, Master, TimeMapping


class PropagateAdmin(object):
    list_display = ['nature', 'activity']
    list_editable = ['nature', 'activity']


class MasterAdmin(object):
    list_display = ['current_week', 'register', 'course']
    list_editable = ['current_week', 'register', 'course']


class TimeMappingAdmin(object):
    list_display = ['class_num', 'time']
    list_editable = ['class_num', 'time']


# 表的注册
xadmin.site.register(Propagate, PropagateAdmin)
xadmin.site.register(Master, MasterAdmin)
xadmin.site.register(TimeMapping, TimeMappingAdmin)
