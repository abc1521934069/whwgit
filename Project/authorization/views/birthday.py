# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from authorization.models import UserInfo
from datetime import date


class BirthdayView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        # 获取生日用户信息
        birthday_date = []
        current_date = date.today()
        users = UserInfo.objects.exclude(judge_invalid=False).order_by("join_time")
        for user in users:
            birthday = user.birthday.replace(year=current_date.year)
            delta = birthday - current_date
            if 0 <= delta.days and delta.days <= 7:
                birthday_date.append({
                    "name": user.name,
                    "sex": 1 if user.sex else 0,
                    "dept": user.userclub.dept.name,
                    "position": user.userclub.position,
                    "college": user.college.name,
                    "birthday": [user.birthday.month, user.birthday.day],
                })
        json_birthday_date = json.dumps(birthday_date)
        # 将生成的级联数据返回
        response_data.append(json_birthday_date)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)
