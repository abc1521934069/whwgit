# -*- encoding=utf8 -*-

import os
from Project import settings
from assists.models import Propagate
from authorization.models import Dept
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin


class IndexInfoView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        # 查询社团首页的图片名字
        images_url = Propagate.objects.filter()
        images = []
        for image in images_url:
            for i in range(1, 6):
                judge_image = getattr(image, 'image' + str(i))
                if judge_image:
                    images.append(str(judge_image)[7:])
        # 获取文件内的所有图片名字
        image_files = os.listdir(settings.MEDIA_URL + 'images')
        response_images = []
        for image_file in image_files:
            if image_file in images:
                response_images.append(image_file)
        response_data.append({
            "images": response_images
        })
        # 获取首页内容
        index_message = Propagate.objects.filter()[0]
        nature = index_message.nature
        activity = index_message.activity
        response_data.append({
            "nature": nature,
            "activity": activity
        })
        # 获取部门名称及推文链接
        response_depts = []
        depts = Dept.objects.exclude(name="社长团").order_by("-dept_id")
        for dept in depts:
            response_depts.append({
                "dept_id": dept.dept_id,
                "name": dept.name
            })
        response_data.append({
            "depts": response_depts
        })
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)
