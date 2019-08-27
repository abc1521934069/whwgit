# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from utils.response import wrap_json_response, ReturnCode
from authorization.models import UserInfo
from apis.models import Comment, Activity


class CommentView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        activity_id = request.GET.get('activity_id')
        activity = Activity.objects.filter(activity_id=activity_id)[0]
        try:
            Comment.objects.filter(activity=activity)[0]
        except:
            judge_exists = False
        if judge_exists:
            comments = []
            comment = []
            temp_comments = Comment.objects.filter(activity=activity).order_by("-time")
            time = temp_comments[0].time.strftime("%Y-%m-%d")
            for temp_comment in temp_comments:
                if temp_comment.time.strftime("%Y-%m-%d") != time:
                    comments.append({
                        "date": time,
                        "message": comment,
                    })
                    comment = []
                    time = temp_comment.time.strftime("%Y-%m-%d")
                    comment.append(temp_comment.message)
                else:
                    comment.append(temp_comment.message)
            comments.append({
                "date": time,
                "message": comment,
            })
            comments.append({
                "date": "End",
                "message": [],
            })
            json_data = json.dumps(comments)
            # 将生成的级联数据返回
            response_data.append(json_data)
            response = self.wrap_json_response(data=response_data)
            return JsonResponse(data=response, safe=False)
        else:
            response = wrap_json_response(data={}, code=ReturnCode.FAILED)
            return JsonResponse(response, safe=False)

    def post(self, request):
        response = {}
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改
        user = UserInfo.objects.filter(user_id=data.get('user_id'))[0]
        activity = Activity.objects.filter(activity_id=data.get('activity_id'))[0]
        Comment.objects.create(activity=activity, user=user, message=data.get('message'))
        # 操作完成
        message = 'add comment successfully.'
        response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
