import xadmin
from .models import Activity, Arrange, Material, Record, Comment, Resource, Article, Image, File


# 类中加入该方法表示去除“删除”功能
# def has_delete_permission(self):
#     return False


class ActivityAdmin(object):
    list_display = ['name', 'begin_w', 'begin_d', 'begin_c', 'end_w', 'end_d', 'end_c', 'address', 'clothes', 'user', 'editor', 'time', 'status', 'judge_delete']
    list_editable = ['name', 'begin_w', 'begin_d', 'begin_c', 'end_w', 'end_d', 'end_c', 'address', 'clothes', 'user', 'status', 'judge_delete']
    exclude = ['activity_id', 'time', 'editor']


class ArrangeAdmin(object):
    list_display = ['activity', 'user', 'begin_w', 'begin_d', 'begin_c', 'end_w', 'end_d', 'end_c', 'message', 'time', 'status', 'editor']
    search_fields = ['message']
    list_filter = ['activity', 'user', 'begin_w', 'begin_d', 'begin_c', 'end_w', 'end_d', 'end_c', 'time', 'status', 'editor']
    list_editable = ['activity', 'user', 'begin_w', 'begin_d', 'begin_c', 'end_w', 'end_d', 'end_c', 'message', 'status']
    exclude = ['arrange_id', 'time', 'editor']


class MaterialAdmin(object):
    list_display = ['activity', 'name', 'count', 'time', 'status', 'editor']
    search_fields = ['name']
    list_filter = ['activity', 'name', 'count', 'time', 'status', 'editor']
    list_editable = ['activity', 'name', 'count', 'status']
    exclude = ['material_id', 'time', 'editor']


class RecordAdmin(object):
    list_display = ['activity', 'recorder', 'user', 'time', 'status']
    list_filter = ['activity', 'recorder', 'user', 'time', 'status']
    list_editable = ['activity', 'user', 'status']
    exclude = ['record_id', 'recorder', 'time']


class CommentAdmin(object):
    list_display = ['activity', 'user', 'message', 'time']
    search_fields = ['message']
    list_filter = ['activity', 'user', 'time']
    exclude = ['comment_id', 'activity', 'user', 'message', 'time']


class ResourceAdmin(object):
    list_display = ['name', 'count']
    search_fields = ['name']
    list_filter = ['name', 'count']
    list_editable = ['name', 'count']
    exclude = ['resource_id']


class ArticleAdmin(object):
    list_display = ['title', 'user', 'time', 'editor']
    search_fields = ['title', 'message']
    list_filter = ['user', 'time', 'editor']
    list_editable = ['title']
    exclude = ['article_id', 'user', 'time', 'editor']


class ImageAdmin(object):
    list_display = ['name', 'user', 'time']
    search_fields = ['name']
    list_filter = ['user', 'time']
    list_editable = ['name']
    exclude = ['image_id', 'time']


class FileAdmin(object):
    list_display = ['name', 'user', 'time']
    search_fields = ['name']
    list_filter = ['user', 'time']
    list_editable = ['name']
    exclude = ['file_id', 'time']


# 表的注册
xadmin.site.register(Activity, ActivityAdmin)
xadmin.site.register(Arrange, ArrangeAdmin)
xadmin.site.register(Material, MaterialAdmin)
xadmin.site.register(Record, RecordAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Resource, ResourceAdmin)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Image, ImageAdmin)
xadmin.site.register(File, FileAdmin)
