# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse

from assists.models import TimeMapping, Master
from utils.response import CommonResponseMixin
from apis.models import Activity, Record, Arrange, Material
from authorization.models import Course, UserInfo, UserClub, Dept
from django.db import transaction
from utils.response import ReturnCode
from django.db.models import Q
from datetime import datetime, timedelta


class ActivityView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        try:
            Activity.objects.filter()[0]
        except:
            judge_exists = False
        if judge_exists:
            activities = []
            if Activity.objects.filter(judge_delete=False).exclude(status=0).count() != 0:
                temp_activities = Activity.objects.filter(judge_delete=False).exclude(status=0).order_by("-status").order_by("-time")
                for activity in temp_activities:
                    activities.append({
                        "id": activity.activity_id,
                        "name": activity.name,
                        "time": activity.time.strftime("%Y-%m-%d"),
                        "begin": [activity.begin_w, activity.begin_d, activity.begin_c],
                        "end": [activity.end_w, activity.end_d, activity.end_c],
                        "address": activity.address,
                        "clothes": activity.clothes,
                        "status": activity.status
                    })
            if Activity.objects.filter(judge_delete=False).filter(status=0).count() != 0:
                temp_activities = Activity.objects.filter(judge_delete=False).filter(status=0).order_by("-time")
                for activity in temp_activities:
                    record = Record.objects.filter(activity=activity)
                    activities.append({
                        "id": activity.activity_id,
                        "name": activity.name,
                        "arrive_need": record.exclude(status=4).count(),
                        "arrive_actual": record.filter(Q(status=2) | Q(status=3)).count(),
                        "arrive_late": record.filter(status=2).count(),
                        "unarrived_request": record.filter(status=1).count(),
                        "unarrived_direct": record.filter(status=0).count(),
                        "status": activity.status
                    })
        else:
            activities = False
        json_activities = json.dumps(activities)
        # 将生成的级联数据返回
        response_data.append(json_activities)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)


class AddActivityView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        try:
            Course.objects.filter()[0]
        except:
            judge_exists = False
        if judge_exists:
            all_course = []
            master = Dept.objects.filter(name="社长团")[0]
            invalid = UserInfo.objects.filter(judge_invalid=False)
            clubs = UserClub.objects.exclude(dept=master).exclude(user__in=invalid).order_by("dept")
            for club in clubs:
                course = club.user.course
                all_course.append({
                    "title": club.user.name + "-" + club.dept.name,
                    "value": club.user.user_id,
                    "courses": {
                        "11": list(map(int, course.mon1[1:-1].split(','))),
                        "12": list(map(int, course.mon2[1:-1].split(','))),
                        "13": list(map(int, course.mon3[1:-1].split(','))),
                        "14": list(map(int, course.mon4[1:-1].split(','))),
                        "15": list(map(int, course.mon5[1:-1].split(','))),
                        "21": list(map(int, course.tue1[1:-1].split(','))),
                        "22": list(map(int, course.tue2[1:-1].split(','))),
                        "23": list(map(int, course.tue3[1:-1].split(','))),
                        "24": list(map(int, course.tue4[1:-1].split(','))),
                        "25": list(map(int, course.tue5[1:-1].split(','))),
                        "31": list(map(int, course.wed1[1:-1].split(','))),
                        "32": list(map(int, course.wed2[1:-1].split(','))),
                        "33": list(map(int, course.wed3[1:-1].split(','))),
                        "34": list(map(int, course.wed4[1:-1].split(','))),
                        "35": list(map(int, course.wed5[1:-1].split(','))),
                        "41": list(map(int, course.thu1[1:-1].split(','))),
                        "42": list(map(int, course.thu2[1:-1].split(','))),
                        "43": list(map(int, course.thu3[1:-1].split(','))),
                        "44": list(map(int, course.thu4[1:-1].split(','))),
                        "45": list(map(int, course.thu5[1:-1].split(','))),
                        "51": list(map(int, course.fri1[1:-1].split(','))),
                        "52": list(map(int, course.fri2[1:-1].split(','))),
                        "53": list(map(int, course.fri3[1:-1].split(','))),
                        "54": list(map(int, course.fri4[1:-1].split(','))),
                        "55": list(map(int, course.fri5[1:-1].split(',')))
                    }
                })
        else:
            all_course = False
        json_all_course = json.dumps(all_course)
        # 将生成的级联数据返回
        response_data.append(json_all_course)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)

    @transaction.atomic
    def post(self, request):
        response = {}
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activity_data = received_body.get('data')
        # 设置回滚点
        RollBackPoint = transaction.savepoint()
        try:
            # 新建活动
            user = UserInfo.objects.filter(user_id=activity_data.get("user_id"))[0]
            activity = Activity.objects.create(
                user=user,
                name=activity_data.get("name"),
                begin_w=activity_data.get("begin_w"),
                begin_d=activity_data.get("begin_d"),
                begin_c=activity_data.get("begin_c"),
                end_w=activity_data.get("end_w"),
                end_d=activity_data.get("end_d"),
                end_c=activity_data.get("end_c"),
                address=activity_data.get("address"),
                clothes=activity_data.get("clothes"),
                message=activity_data.get("message")
            )
            # 获取当前活动已记录的签到表
            user_list = []
            record_all = Record.objects.filter(activity=activity).values("user__user_id")
            for record in record_all:
                user_list.append(record.user_id)
            # 新建工作安排
            job_list = []
            record_list = []
            jobs = activity_data.get("jobs")
            for job in jobs:
                for user_id in job["ids"]:
                    temp_user = UserInfo.objects.filter(user_id=user_id)[0]
                    temp_job = Arrange(
                        activity=activity,
                        user=temp_user,
                        begin_w=job["begin_time"][0] + 1,
                        begin_d=job["begin_time"][1] + 1,
                        begin_c=job["begin_time"][2] + 1,
                        end_w=job["end_time"][0] + 1,
                        end_d=job["end_time"][1] + 1,
                        end_c=job["end_time"][2] + 1,
                        message=job["message"]
                    )
                    if user_id not in user_list:
                        user_list.append(user_id)
                        temp_record = Record(
                            activity=activity,
                            user=temp_user
                        )
                        record_list.append(temp_record)
                    job_list.append(temp_job)
            Arrange.objects.bulk_create(job_list)
            Record.objects.bulk_create(record_list)
            # 新建物资需求和签到
            resource_list = []
            material = activity_data.get("material")
            for resource in material:
                temp_resource = Material(
                    activity=activity,
                    name=resource["name"],
                    count=resource["count"]
                )
                resource_list.append(temp_resource)
            Material.objects.bulk_create(resource_list)
            transaction.savepoint_commit(RollBackPoint)
            # 操作完成
            message = 'add activity successfully.'
            response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
            return JsonResponse(response, safe=False)
        except:
            transaction.savepoint_rollback(RollBackPoint)
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)


class ActivityPageView(View, CommonResponseMixin):
    def post(self, request):
        response_data = []
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activity_id = received_body.get('data')
        # 获取活动信息
        activity = []
        temp_activity = Activity.objects.filter(activity_id=activity_id)[0]
        activity.append({
            "title": temp_activity.name,
            "begin_time": [temp_activity.begin_w - 1, temp_activity.begin_d - 1, temp_activity.begin_c - 1],
            "end_time": [temp_activity.end_w - 1, temp_activity.end_d - 1, temp_activity.end_c - 1],
            "activity_address": temp_activity.address,
            "clothes": temp_activity.clothes,
            "activity_process": temp_activity.message
        })
        # 获取工作安排
        job_list = []
        if Arrange.objects.filter(activity=temp_activity).count() != 0:
            jobs = Arrange.objects.filter(activity=temp_activity).order_by("status")
            arrange_id = []
            begin_w = jobs[0].begin_w
            begin_d = jobs[0].begin_d
            begin_c = jobs[0].begin_c
            end_w = jobs[0].end_w
            end_d = jobs[0].end_d
            end_c = jobs[0].end_c
            message = jobs[0].message
            users = ""
            finish = jobs[0].status
            for job in jobs:
                if (begin_w == job.begin_w
                    and begin_d == job.begin_d
                    and begin_c == job.begin_c
                    and end_w == job.end_w
                    and end_d == job.end_d
                    and end_c == job.end_c
                    and message == job.message
                    and finish == job.status):
                    arrange_id.append(job.arrange_id)
                    users += job.user.name + "\n"
                else:
                    job_list.append({
                        "ids": arrange_id,
                        "begin_time": [begin_w - 1, begin_d - 1, begin_c - 1],
                        "end_time": [end_w - 1, end_d - 1, end_c - 1],
                        "message": message,
                        "value": users,
                        "finish": finish
                    })
                    arrange_id = [job.arrange_id]
                    begin_w = job.begin_w
                    begin_d = job.begin_d
                    begin_c = job.begin_c
                    end_w = job.end_w
                    end_d = job.end_d
                    end_c = job.end_c
                    message = job.message
                    users = job.user.name + "\n"
                    finish = job.status
            # 放入最后一组工作安排
            job_list.append({
                "ids": arrange_id,
                "begin_time": [begin_w - 1, begin_d - 1, begin_c - 1],
                "end_time": [end_w - 1, end_d - 1, end_c - 1],
                "message": message,
                "value": users,
                "finish": finish
            })
        activity.append(job_list)
        # 获取物资需求
        resource_list = []
        if Material.objects.filter(activity=temp_activity).count() != 0:
            material = Material.objects.filter(activity=temp_activity).order_by("status")
            for resource in material:
                resource_list.append({
                    "material_id": resource.material_id,
                    "name": resource.name,
                    "count": resource.count,
                    "finish": resource.status
                })
        activity.append(resource_list)
        # 操作完成
        json_activity = json.dumps(activity)
        # 将生成的级联数据返回
        response_data.append(json_activity)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)


class EditBasicView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activityInfo_data = received_body.get('data')
        # 修改活动信息
        user = UserInfo.objects.filter(user_id=activityInfo_data.get("user_id"))[0]
        activity = Activity.objects.filter(activity_id=activityInfo_data.get("activity_id"))[0]
        activity.name = activityInfo_data.get("name")
        activity.begin_w = activityInfo_data.get("begin_w")
        activity.begin_d = activityInfo_data.get("begin_d")
        activity.begin_c = activityInfo_data.get("begin_c")
        activity.end_w = activityInfo_data.get("end_w")
        activity.end_d = activityInfo_data.get("end_d")
        activity.end_c = activityInfo_data.get("end_c")
        activity.address = activityInfo_data.get("address")
        activity.clothes = activityInfo_data.get("clothes")
        activity.editor = user
        activity.save()
        # 操作完成
        message = 'edit the activity basic successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class EditMessageView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activityMessage_data = received_body.get('data')
        # 修改活动信息
        user = UserInfo.objects.filter(user_id=activityMessage_data.get("user_id"))[0]
        activity = Activity.objects.filter(activity_id=activityMessage_data.get("activity_id"))[0]
        activity.message = activityMessage_data.get("message")
        activity.editor = user
        activity.save()
        # 操作完成
        message = 'edit the activity message successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class AddArrangeView(View, CommonResponseMixin):
    @transaction.atomic
    def post(self, request):
        response_data = []
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activity_data = received_body.get('data')
        # 设置回滚点
        RollBackPoint = transaction.savepoint()
        try:
            arrange_id = []
            # 获取信息
            user = UserInfo.objects.filter(user_id=activity_data.get("user_id"))[0]
            activity = Activity.objects.filter(activity_id=activity_data.get("activity_id"))[0]
            workers = activity_data.get("ids")
            # 获取当前活动已记录的签到表
            user_list = []
            record_all = Record.objects.filter(activity=activity).values("user__user_id")
            for record in record_all:
                user_list.append(record["user__user_id"])
            # 新建工作安排
            job_list = []
            record_list = []
            for user_id in workers:
                temp_user = UserInfo.objects.filter(user_id=user_id)[0]
                temp_job = Arrange(
                    activity=activity,
                    user=temp_user,
                    begin_w=activity_data.get("begin_time")[0] + 1,
                    begin_d=activity_data.get("begin_time")[1] + 1,
                    begin_c=activity_data.get("begin_time")[2] + 1,
                    end_w=activity_data.get("end_time")[0] + 1,
                    end_d=activity_data.get("end_time")[1] + 1,
                    end_c=activity_data.get("end_time")[2] + 1,
                    message=activity_data.get("message"),
                    editor=user
                )
                if user_id not in user_list:
                    temp_record = Record(
                        activity=activity,
                        user=temp_user
                    )
                    record_list.append(temp_record)
                job_list.append(temp_job)
            arranges = Arrange.objects.bulk_create(job_list)
            for arrange in arranges:
                arrange_id.append(arrange.arrange_id)
            Record.objects.bulk_create(record_list)
            transaction.savepoint_commit(RollBackPoint)
            # 操作完成
            json_add_job = json.dumps(arrange_id)
            # 将生成的级联数据返回
            response_data.append(json_add_job)
            response = self.wrap_json_response(data=response_data)
            return JsonResponse(data=response, safe=False)
        except:
            transaction.savepoint_rollback(RollBackPoint)
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)


class EditArrangeView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activityArrange_data = received_body.get('data')
        # 修改工作安排
        user = UserInfo.objects.filter(user_id=activityArrange_data.get("user_id"))[0]
        arranges = Arrange.objects.filter(arrange_id__in=activityArrange_data.get("arrange_id"))
        arranges.update(message=activityArrange_data.get("message"), editor=user, status=False)
        # 操作完成
        message = 'edit the activity arrange successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)

    @transaction.atomic
    def delete(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activityArrange_data = received_body.get('data')
        # 设置回滚点
        RollBackPoint = transaction.savepoint()
        try:
            # 删除工作安排
            Arrange.objects.filter(arrange_id__in=activityArrange_data.get("arrange_id")).delete()
            # 获取当前活动有任务安排的成员
            user_list = []
            activity = Activity.objects.filter(activity_id=activityArrange_data.get("activity_id"))[0]
            arrange_all = Arrange.objects.filter(activity=activity).values("user")
            for arrange in arrange_all:
                user_id = arrange["user"]
                if user_id not in user_list:
                    user_list.append(user_id)
            # 删除签到表中没工作安排的记录
            Record.objects.filter(activity=activity).exclude(user__user_id__in=user_list).delete()
            # 提交
            transaction.savepoint_commit(RollBackPoint)
            # 操作完成
            message = 'delete the activity arrange successfully.'
            response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
            return JsonResponse(response, safe=False)
        except:
            transaction.savepoint_rollback(RollBackPoint)
            response = self.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)


class FinishActivityArrangeView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        finishArrange_data = received_body.get('data')
        # 完成任务安排
        user = UserInfo.objects.filter(user_id=finishArrange_data.get("user_id"))[0]
        arranges = Arrange.objects.filter(arrange_id__in=finishArrange_data.get("arrange_id"))
        arranges.update(editor=user, status=True)
        # 获取当前时间
        current_week = Master.objects.first().current_week
        current_day = int(datetime.now().strftime("%w"))
        current_time = int(datetime.now().strftime("%H%M%S"))
        for arrange in arranges:
            status = "finish"
            # 获取活动时间
            end_week = arrange.end_w
            end_day = arrange.end_d
            end_time = int(TimeMapping.objects.filter(class_num=arrange.end_c + 1)[0].time.strftime("%H%M%S"))
            # 时间判断
            if current_week >= end_week and current_day >= end_day and current_time > end_time:
                status = "overtime"
            # 进行工作记录
            user_record = arrange.user.userrecord
            user_record.__dict__[status] += 1
            user_record.save()
        # 操作完成
        message = 'finish the activity arrange successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class AddMaterialView(View, CommonResponseMixin):
    def post(self, request):
        response_data = []
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activity_data = received_body.get('data')
        arrange_id = []
        # 获取信息
        user = UserInfo.objects.filter(user_id=activity_data.get("user_id"))[0]
        activity = Activity.objects.filter(activity_id=activity_data.get("activity_id"))[0]
        material = Material.objects.create(activity=activity, name=activity_data.get("name"), count=activity_data.get("count"), editor=user)
        # 操作完成
        json_add_material = json.dumps(material.material_id)
        # 将生成的级联数据返回
        response_data.append(json_add_material)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)


class EditMaterialView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activityMaterial_data = received_body.get('data')
        # 修改物资需求
        user = UserInfo.objects.filter(user_id=activityMaterial_data.get("user_id"))[0]
        material = Material.objects.filter(material_id=activityMaterial_data.get("material_id"))[0]
        material.count = activityMaterial_data.get("count")
        material.editor = user
        material.status = False
        material.save()
        # 操作完成
        message = 'edit the activity material successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)

    def delete(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        activityMaterial_data = received_body.get('data')
        # 删除物资需求
        Material.objects.filter(material_id=activityMaterial_data.get("material_id")).delete()
        # 操作完成
        message = 'delete the activity material successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class FinishActivityMaterialView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        finishMaterial_data = received_body.get('data')
        # 完成物资需求
        user = UserInfo.objects.filter(user_id=finishMaterial_data.get("user_id"))[0]
        material = Material.objects.filter(material_id=finishMaterial_data.get("material_id"))
        material.update(editor=user, status=True)
        # 操作完成
        message = 'finish the activity material successfully.'
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
