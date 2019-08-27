# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from utils.response import wrap_json_response, ReturnCode
from authorization.models import UserInfo, Register, Dept, UserClub, UserPower, UserRecord
from django.db.models import Q
from django.db import transaction


class RegisterManageView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        # 获取报名人员信息
        judge_exists = True
        user_id = request.GET.get('user_id')
        dept = UserInfo.objects.filter(user_id=user_id)[0].userclub.dept
        try:
            if dept.name == "社长团":
                Register.objects.all()[0]
            else:
                Register.objects.filter(Q(dept1=dept) | Q(dept2=dept))[0]
        except:
            judge_exists = False
        if judge_exists:
            registers = []
            if dept.name == "社长团":
                temp_registers = Register.objects.all()
            else:
                temp_registers = Register.objects.filter(Q(dept1=dept) | Q(dept2=dept))
            for temp_register in temp_registers:
                registers.append({
                    "user_id": temp_register.user.user_id,
                    "name": temp_register.user.name,
                    "sex": 1 if temp_register.user.sex else 0,
                    "phone": temp_register.user.phone,
                    "dept": temp_register.dept1.name + (('、' + temp_register.dept2.name) if temp_register.dept2 else ''),
                    "college": temp_register.user.college.name,
                    "introduce": temp_register.user.introduce,
                    "select": False,
                    "style": ""
                })
            json_data = json.dumps(registers)
            response_data.append(json_data)
            # 获取部门选项
            depts = []
            options = []
            temp_depts = Dept.objects.exclude(name="社长团")
            for dept in temp_depts:
                depts.append([dept.dept_id, dept.name])
                options.append("聘用为" + dept.name + "干事")
            options.append("婉拒申请")
            json_options = json.dumps(options)
            response_data.append(json_options)
            json_depts = json.dumps(depts)
            response_data.append(json_depts)
        else:
            response_data.append(False)
        # 将生成的级联数据返回
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)

    @transaction.atomic
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 设置回滚点
        RollBackPoint = transaction.savepoint()
        try:
            # 聘用操作
            users = UserInfo.objects.filter(user_id__in=data.get('user_id'))
            dept = Dept.objects.filter(dept_id=data.get('dept_id'))[0]
            Register.objects.filter(user__in=users).delete()
            for user in users:
                UserInfo.objects.filter(user_id=user.user_id).update(judge_invalid=True)
                UserClub.objects.create(user=user, dept=dept)
                UserPower.objects.create(user=user)
                UserRecord.objects.create(user=user)
            # 操作完成
            transaction.savepoint_commit(RollBackPoint)
            message = 'operate successfully.'
            response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
            return JsonResponse(response, safe=False)
        except:
            transaction.savepoint_rollback(RollBackPoint)
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)

    def delete(self, request):
        response = {}
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 删除用户
        UserInfo.objects.filter(user_id__in=data.get('user_id')).delete()
        # 操作完成
        message = 'delete successfully.'
        response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
