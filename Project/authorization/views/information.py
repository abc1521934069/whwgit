# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin, ReturnCode
from authorization.models import UserClub, Dept, UserInfo, UserPower


class ClubInfoView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        try:
            UserClub.objects.filter()[0]
        except:
            judge_exists = False
        if judge_exists:
            info = []
            # 获取成员信息
            member_info = []
            invalid = UserInfo.objects.filter(judge_invalid=False)
            clubs = UserClub.objects.exclude(user__in=invalid).order_by("-dept")
            for club in clubs:
                member_info.append({
                    "user_id": club.user.user_id,
                    "name": club.user.name,
                    "sex": 1 if club.user.sex else 0,
                    "phone": club.user.phone,
                    "dept": [club.dept.dept_id, club.dept.name],
                    "position": club.position,
                    "college": club.user.college.name,
                    "add_activity": club.user.userpower.add_activity,
                    "edit_activity": club.user.userpower.edit_activity,
                    "add_article": club.user.userpower.add_article,
                    "edit_article": club.user.userpower.edit_article,
                    "edit_course": club.user.userpower.edit_course,
                    "record": club.user.userpower.record,
                    "add_file": club.user.userpower.add_file,
                    "add_image": club.user.userpower.add_image,
                    "stay": club.judge_remain
                })
            info.append(member_info)
            # 获取部门筛选信息
            depts_info = []
            depts = Dept.objects.all()
            for dept in depts:
                depts_info.append({
                    "label": dept.name,
                    "value": str(dept.dept_id)
                })
            info.append(depts_info)
        else:
            info = False
        json_info = json.dumps(info)
        # 将生成的级联数据返回
        response_data.append(json_info)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)


class PowerEditView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改权限信息
        users = UserInfo.objects.filter(user_id__in=data.get("user_id"))
        users_power = UserPower.objects.filter(user__in=users)
        for user in users_power:
            user.__dict__[data.get("power")] = True
            user.save()
        # 操作完成
        message = 'add the power successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)

    def delete(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改权限信息
        power = UserInfo.objects.filter(user_id=data.get("user_id"))[0].userpower
        power.__dict__[data.get("power")] = False
        power.save()
        # 操作完成
        message = 'delete the power successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class SpeciaRemainView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改留任信息
        users = UserInfo.objects.filter(user_id__in=data.get("user_id"))
        users_club = UserClub.objects.filter(user__in=users)
        for club in users_club:
            if club.position == 1:
                club.dept = Dept.objects.filter(name="社长团")[0]
                club.position = 2
            else:
                club.position = 1
                UserPower.objects.filter(user=club.user).update(
                    add_activity=True,
                    edit_activity=True,
                    record=True,
                    edit_course=True,
                    add_article=True,
                    edit_article=True,
                    add_image=True,
                    add_file=True
                )
            club.judge_remain = True
            club.save()
        # 操作完成
        message = 'edit the remian successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)

    def delete(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改留任信息
        club = UserInfo.objects.filter(user_id=data.get("user_id"))[0].userclub
        club.position = 0
        club.judge_remain = False
        club.save()
        UserPower.objects.filter(user=club.user).update(
            add_activity=False,
            edit_activity=False,
            record=False,
            edit_course=False,
            add_article=False,
            edit_article=False,
            add_image=False,
            add_file=False
        )
        # 操作完成
        message = 'edit the remian successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class SpeciaDeleteView(View, CommonResponseMixin):
    def delete(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改留任信息
        users = UserInfo.objects.filter(user_id__in=data.get("user_id"))
        for user in users:
            user.__dict__["judge_invalid"] = False
            user.save()
        # 操作完成
        message = 'expel the member successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
