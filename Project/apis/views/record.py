# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse

from apis.models import Activity, Arrange
from assists.models import TimeMapping, Master
from utils.response import CommonResponseMixin, ReturnCode
from authorization.models import Dept, UserInfo, UserRecord
from apis.models import Record
from datetime import datetime, timedelta
from django.db.models import F


class RecordView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        activity_id = request.GET.get('activity_id')
        activity = Activity.objects.filter(activity_id=activity_id)[0]
        try:
            Record.objects.filter(activity=activity)[0]
        except:
            judge_exists = False
        if judge_exists:
            info = []
            # 获取成员信息
            member_info = []
            records = Record.objects.filter(activity=activity, status=5)
            for record in records:
                member_info.append({
                    "user_id": record.user.user_id,
                    "name": record.user.name,
                    "sex": 1 if record.user.sex else 0,
                    "phone": record.user.phone,
                    "dept": [record.user.userclub.dept.dept_id, record.user.userclub.dept.name],
                    "position": record.user.userclub.position
                })
            info.append(member_info)
            # 获取部门筛选信息
            depts_info = []
            depts = Dept.objects.exclude(name="社长团")
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

    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 获取基本数据
        activity = Activity.objects.filter(activity_id=data.get("activity_id"))[0]
        users = UserInfo.objects.filter(user_id__in=data.get("user_id"))
        # 获取当前时间
        current_time = int(datetime.now().strftime("%H%M%S"))
        # 获取活动时间
        begin_time = TimeMapping.objects.filter(class_num=activity.begin_c)[0].time
        delta = timedelta(minutes=15)
        begin_time = int((begin_time+delta).strftime("%H%M%S"))
        end_time = int(TimeMapping.objects.filter(class_num=activity.end_c + 1)[0].time.strftime("%H%M%S"))
        # 能签到时已经进入活动时间前半小时
        status = 3
        if current_time >= begin_time +1500 and current_time < end_time:
            UserRecord.objects.filter(user__in=users).update(late=F("late") + 1)
            status = 2
        if not data.get("oper"):
            UserRecord.objects.filter(user__in=users).update(request=F("request") + 1)
            status = 1
        Record.objects.filter(activity=activity, user__in=users).update(status=status)
        # 操作完成
        message = 'record successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)

    def delete(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 忽略操作
        activity = Activity.objects.filter(activity_id=data.get("activity_id"))[0]
        users = UserInfo.objects.filter(user_id__in=data.get("user_id"))
        Record.objects.filter(user__in=users, activity=activity).update(status=4)
        # 操作完成
        message = 'ignore successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
