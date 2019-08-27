# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from authorization.models import UserInfo
from utils.response import wrap_json_response, ReturnCode


class PersonalInfoView(View, CommonResponseMixin):
    def post(self, request):
        response_data = []
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        personal_data = received_body.get('data')
        # 获取用户信息
        user = UserInfo.objects.filter(user_id=personal_data.get("user_id"))[0]
        personal_info = {
            "name": user.name,
            "sex": user.sex,
            "dept": user.userclub.dept.name,
            "college": user.college.name,
            "major": user.major.name,
            "grade": user.grade,
            "class_num": user.class_num,
            "phone": user.phone,
            "address": user.address
        }
        json_personal_info = json.dumps(personal_info)
        # 将生成的级联数据返回
        response_data.append(json_personal_info)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)


class PersonalInfoEditView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        edit_data = received_body.get('data')
        # 获取用户
        user = UserInfo.objects.filter(user_id=edit_data.get("user_id"))[0]
        user.phone = edit_data.get("phone")
        user.address = edit_data.get("address")
        user.save()
        # 操作完成
        message = 'edit the personal information successfully.'
        response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
