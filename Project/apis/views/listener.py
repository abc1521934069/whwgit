# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from assists.models import TimeMapping, Master
from utils.response import CommonResponseMixin
from apis.models import Record, Activity, Arrange
from datetime import datetime, timedelta


class RecordListenerView(View, CommonResponseMixin):
    def get(self, request):
        # False表示活动未结束
        judge = False
        # 获取基本数据
        activity = Activity.objects.filter(activity_id=request.GET.get("activity_id"))[0]
        # 获取当前时间
        current_time = int(datetime.now().strftime("%H%M%S"))
        # 获取活动时间
        end_time = int(TimeMapping.objects.filter(class_num=activity.end_c + 1)[0].time.strftime("%H%M%S"))
        if current_time >= end_time:
            records = Record.objects.filter(activity=activity, status=5)
            records.update(status=0)
            for record in records:
                user_record = record.user.userrecord
                user_record.absent += 1
                user_record.save()
            for arrange in Arrange.objects.filter(activity=activity, status=False):
                user_record = arrange.user.userrecord
                user_record.incomplete += 1
                user_record.save()
            activity.status = 0
            activity.save()
            judge = True
        json_data = json.dumps(judge)
        # 将生成的级联数据返回
        response = self.wrap_json_response(data=json_data)
        return JsonResponse(data=response, safe=False)


class ActivityListenerView(View, CommonResponseMixin):
    def get(self, request):
        # False表示没有活动改变当前状态
        judge = False
        # 获取当前时间
        current_week = Master.objects.first().current_week
        current_day = int(datetime.now().strftime("%w"))
        current_time = int(datetime.now().strftime("%H%M%S"))
        # 进行活动检测
        for activity in Activity.objects.exclude(status=0):
            # 获取活动时间
            begin_time = TimeMapping.objects.filter(class_num=activity.begin_c)[0].time
            delta = timedelta(minutes=30)
            begin_time = int((begin_time-delta).strftime("%H%M%S"))
            end_time = int(TimeMapping.objects.filter(class_num=activity.end_c + 1)[0].time.strftime("%H%M%S"))
            if current_week == activity.begin_w and current_day == activity.begin_d:
                if activity.status == 1 and current_time >= begin_time:
                    activity.status = 2
                    activity.save()
                    judge = True
                if current_time >= end_time:
                    for record in Record.objects.filter(activity=activity, status=5):
                        user_record = record.user.userrecord
                        user_record.absent += 1
                        user_record.save()
                    for arrange in Arrange.objects.filter(activity=activity, status=False):
                        user_record = arrange.user.userrecord
                        user_record.incomplete += 1
                        user_record.save()
                    activity.status = 0
                    activity.save()
                    judge = True
        for activity in Activity.objects.filter(status=0, judge_delete=False):
            if current_week >= activity.end_w + 1:
                activity.judge_delete = True
                activity.save()
                judge = True
        json_data = json.dumps(judge)
        # 将生成的级联数据返回
        response = self.wrap_json_response(data=json_data)
        return JsonResponse(data=response, safe=False)
