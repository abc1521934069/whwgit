# -*- coding=utf-8 -*-

from django.urls import path

from authorization.views import authorization, register, personal_info, course, information, birthday, register_manage, dept


urlpatterns = [
    path(r'authorize', authorization.authorize, name='authorize'),
    path(r'register', register.RegisterView.as_view(), name='register'),
    path(r'personal', personal_info.PersonalInfoView.as_view(), name='personal'),
    path(r'editPersonal', personal_info.PersonalInfoEditView.as_view(), name='editPersonal'),
    path(r'course', course.CourseView.as_view(), name='course'),
    path(r'editCourse', course.CourseEditView.as_view(), name='editCourse'),
    path(r'clubInfo', information.ClubInfoView.as_view(), name='clubInfo'),
    path(r'powerEdit', information.PowerEditView.as_view(), name='powerEdit'),
    path(r'specialRemain', information.SpeciaRemainView.as_view(), name='specialRemain'),
    path(r'specialDelete', information.SpeciaDeleteView.as_view(), name='specialDelete'),
    path(r'birthday', birthday.BirthdayView.as_view(), name='birthday'),
    path(r'register_manage', register_manage.RegisterManageView.as_view(), name='register_manage'),
    path(r'dept', dept.DeptView.as_view(), name='dept')
]