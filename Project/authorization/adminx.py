import xadmin
from .models import College, Major, Dept, UserInfo, Register, UserClub, UserPower, UserRecord, Course
from xadmin.views import BaseAdminView, CommAdminView


# 表的定义
class CollegeAdmin(object):
    list_display = ['college_id', 'name']
    search_fields = ['college_id', 'name']
    list_filter = ['college_id', 'name']
    list_editable = ['name']


class MajorAdmin(object):
    list_display = ['major_id', 'college', 'name']
    search_fields = ['major_id', 'name']
    list_filter = ['major_id', 'college', 'name']
    list_editable = ['name']


class DeptAdmin(object):
    list_display = ['dept_id', 'name']
    search_fields = ['dept_id', 'name']
    list_filter = ['dept_id', 'name']
    list_editable = ['name']


class UserInfoAdmin(object):
    list_display = ['name', 'phone', 'address', 'birthday', 'sex', 'college', 'major', 'grade', 'class_num', 'dorm', 'dorm_num', 'join_time', 'judge_invalid']
    search_fields = ['name', 'phone', 'address', 'grade']
    list_filter = ['address', 'birthday', 'sex', 'college', 'major', 'grade', 'class_num', 'dorm', 'dorm_num', 'introduce', 'join_time', 'judge_invalid']
    list_editable = ['name', 'phone', 'address', 'birthday', 'sex', 'college', 'major', 'grade', 'class_num', 'dorm', 'dorm_num', 'judge_invalid']
    exclude = ['user_id', 'openid', 'join_time']


class RegisterAdmin(object):
    list_display = ['user', 'dept1', 'dept2', 'register_time']
    list_filter = ['dept1', 'dept2', 'register_time']
    list_editable = ['dept1', 'dept2']
    exclude = ['register_time']


class UserClubAdmin(object):
    list_display = ['user', 'dept', 'position', 'judge_remain']
    list_filter = ['dept', 'position', 'judge_remain']
    list_editable = ['dept', 'position', 'judge_remain']


class UserPowerAdmin(object):
    list_display = ['user', 'add_activity', 'edit_activity', 'record', 'edit_course', 'add_article', 'edit_article', 'add_image', 'add_file']
    list_filter = ['add_activity', 'edit_activity', 'record', 'edit_course', 'add_article', 'edit_article', 'add_image', 'add_file']
    list_editable = ['add_activity', 'edit_activity', 'record', 'edit_course', 'add_article', 'edit_article', 'add_image', 'add_file']


class UserRecordAdmin(object):
    list_display = ['user', 'late', 'request', 'absent', 'finish', 'overtime', 'incomplete']
    list_filter = ['late', 'request', 'absent', 'finish', 'overtime', 'incomplete']
    list_editable = ['late', 'request', 'absent', 'finish', 'overtime', 'incomplete']


class CourseAdmin(object):
    list_display = ['user']
    exclude = ['course_id']


# 表的注册
xadmin.site.register(College, CollegeAdmin)
xadmin.site.register(Major, MajorAdmin)
xadmin.site.register(Dept, DeptAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(Register, RegisterAdmin)
xadmin.site.register(UserClub, UserClubAdmin)
xadmin.site.register(UserPower, UserPowerAdmin)
xadmin.site.register(UserRecord, UserRecordAdmin)
xadmin.site.register(Course, CourseAdmin)


# 页面配置
class ThemeSetting(object):
    """配置主题"""
    enable_themes = True
    use_bootswatch = True


class CustomView(object):
    # 网页头部导航
    site_title = '社团后台管理'
    # 底部版权
    site_footer = '营销达人社'
    # 左侧导航折叠筐
    # 列表显示
    # one：只显示一条
    # accordion：缩略列表显示，可下拉
    # tab：横向tab显示
    # stacked：块显示
    # table：列表
    menu_style = 'accordion'


# 对配置进行注册
xadmin.site.register(BaseAdminView, ThemeSetting)
xadmin.site.register(CommAdminView, CustomView)
