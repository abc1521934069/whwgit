# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from authorization.models import College, Major, Dept, UserInfo, Register
from utils.response import wrap_json_response, ReturnCode
from datetime import datetime


class RegisterView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        # 班级选择信息
        data_class = []
        # 班级
        class_num = [
            {
                "label": "01班",
                "value": "01"
            },
            {
                "label": "02班",
                "value": "02"
            },
            {
                "label": "03班",
                "value": "03"
            },
            {
                "label": "04班",
                "value": "04"
            },
            {
                "label": "05班",
                "value": "05"
            },
            {
                "label": "06班",
                "value": "06"
            },
            {
                "label": "07班",
                "value": "07"
            },
            {
                "label": "08班",
                "value": "08"
            },
            {
                "label": "09班",
                "value": "09"
            },
            {
                "label": "10班",
                "value": "10"
            }
        ]
        # 年级
        grade = []
        current_year = int(datetime.now().strftime('%Y')[-2:])
        for i in range(current_year-3, current_year+2):
            grade.append({
                "label": str(i),
                "value": str(i),
                "children": class_num
            })
        # 学院和专业
        colleges = College.objects.all()
        for college in colleges:
            temp_college = {
                "label": college.name,
                "value": str(college.college_id),
                "children": []
            }
            for major in college.major_set.all():
                temp_college["children"].append({
                    "label": major.name,
                    "value": major.major_id,
                    "children": grade
                })
            data_class.append(temp_college)
        # 将生成的班级选择数据加入返回数据
        response_data.append(data_class)
        # 部门
        data_dept = []
        depts = Dept.objects.exclude(name="社长团")
        for dept in depts:
            data_dept.append({
                "title": dept.name,
                "value": str(dept.dept_id),
            })
        # 将生成的班级选择数据加入返回数据
        response_data.append(data_dept)
        # 将生成的级联数据返回
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        response = {}
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        register_data = received_body.get('data')
        # 修改用户信息
        user = UserInfo.objects.filter(user_id=register_data.get("user_id"))[0]
        user.name = register_data.get("name")
        user.phone = register_data.get("phone")
        user.address = register_data.get("address")
        user.birthday = datetime(
            register_data.get("birthday")[0],
            register_data.get("birthday")[1],
            register_data.get("birthday")[2]
        )
        user.sex = True if int(register_data.get("sex")) else False
        user.college = College.objects.filter(college_id=register_data.get("value_class")[0])[0]
        user.major = Major.objects.filter(major_id=register_data.get("value_class")[1])[0]
        user.grade = register_data.get("value_class")[2]
        user.class_num = register_data.get("value_class")[3]
        user.dorm = register_data.get("dorm")[0]
        user.dorm_num = register_data.get("dorm")[1]
        user.introduce = register_data.get("user_id")
        user.save()
        # 加入注册
        register = Register(
            user=user,
            dept1=Dept.objects.filter(dept_id=register_data.get("depts")[0])[0]
        )
        if len(register_data.get("depts")) == 2:
            register.dept2 = Dept.objects.filter(dept_id=register_data.get("depts")[1])[0]
        register.save()
        if (not UserInfo.objects.filter(user_id=register_data.get("user_id"))) or (not Register.objects.filter(user=user)):
            response['result_code'] = ReturnCode.FAILED
            response['message'] = 'register error.'
            return JsonResponse(response, safe=False)
        # 操作完成
        message = 'user register successfully.'
        response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
