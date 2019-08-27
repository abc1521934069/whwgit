# -*- encoding=utf8 -*-

from utils.wx.code2session import code2session


def c2s(appid, code):
    return code2session(appid, code)


class AccountInfo:
    def __init__(self, id):
        self.user_id = id
        self.register = False
        self.status = False
        self.position = 0
        self.add_activity = False
        self.edit_activity = False
        self.record = False
        self.edit_course = False
        self.add_article = False
        self.edit_article = False
        self.add_image = False
        self.add_file = False
        self.all_register = False
        self.all_course = False

    def set_status(self, register, status):
        self.register = register
        self.status = status

    def set_power(self, user):
        self.add_activity = user.add_activity
        self.edit_activity = user.edit_activity
        self.record = user.record
        self.edit_course = user.edit_course
        self.add_article = user.add_article
        self.edit_article = user.edit_article
        self.add_image = user.add_image
        self.add_file = user.add_file

    def set_position(self, user):
        self.position = user.position

    def set_global(self, user):
        self.all_register = user.register
        self.all_course = user.course
        self.current_week = user.current_week
