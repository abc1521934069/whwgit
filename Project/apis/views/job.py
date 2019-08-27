# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from authorization.models import UserInfo
from apis.models import Arrange, Activity


class JobView(View, CommonResponseMixin):
    def post(self, request):
        response_data = []
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        personal_data = received_body.get('data')
        # 获取用户信息
        judge_exists = True
        user = UserInfo.objects.filter(user_id=personal_data.get("user_id"))[0]
        try:
            Arrange.objects.filter(user=user)[0]
        except:
            judge_exists = False
        if judge_exists:
            activities = []
            temp_activities = Activity.objects.exclude(status=0)
            for activity in temp_activities:
                temp_activity = {
                    "name": activity.name,
                    "begin": [activity.begin_w, activity.begin_d, activity.begin_c],
                    "end": [activity.end_w, activity.end_d, activity.end_c],
                    "address": activity.address,
                    "clothes": activity.clothes,
                    "job": []
                }
                jobs = activity.arrange_set.filter(user=user).order_by("status")
                for job in jobs:
                    temp_activity["job"].append({
                        "begin": [job.begin_w, job.begin_d, job.begin_c],
                        "end": [job.end_w, job.end_d, job.end_c],
                        "message": job.message,
                        "status": job.status,
                    })
                activities.append(temp_activity)
        else:
            activities = False
        json_activities = json.dumps(activities)
        # 将生成的级联数据返回
        response_data.append(json_activities)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)
