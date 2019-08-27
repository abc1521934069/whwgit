# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse

from assists.models import Master
from utils.response import CommonResponseMixin
from utils.response import wrap_json_response, ReturnCode


class SpecialPowerView(View, CommonResponseMixin):
    def post(self, request):
        response = {}
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        data = received_body.get('data')
        # 修改
        master = Master.objects.filter()[0]
        master.__dict__[data.get("field")] = data.get("change_status")
        master.save()
        # 操作完成
        message = 'edit master successfully.'
        response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
