# -*- encoding=utf8 -*-

import os
from Project import settings
from django.views import View
from django.http import FileResponse
from utils.response import CommonResponseMixin


class ImageView(View, CommonResponseMixin):
    def get(self, request):
        name = request.GET.get('name')
        imgfile = os.path.join(settings.IMAGES_DIR, name)
        return FileResponse(open(imgfile, 'rb'), content_type='image/*')
