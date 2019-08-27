# -*- coding=utf-8 -*-

import os
from Project import settings
from assists.models import Propagate
from authorization.models import Dept
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin


class DeptView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        dept_id = request.GET.get('dept_id')
        # 获取页面内容
        dept = Dept.objects.filter(dept_id=dept_id)[0]
        content = []
        content.append({
            "name": "介绍",
            "content": dept.introduce
        })
        content.append({
            "name": "职能",
            "content": dept.technology
        })
        content.append({
            "name": "工作",
            "content": dept.work
        })
        content.append({
            "name": "日常",
            "content": dept.daily
        })
        response_data.append({"name": dept.name})
        response_data.append(content)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)
