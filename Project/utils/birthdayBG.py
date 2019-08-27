# -*- coding=utf-8 -*-

import os
from Project import settings
from django.views import View
from django.http import FileResponse
from utils.response import CommonResponseMixin


class BirthdayBackgroundView(View, CommonResponseMixin):
    def get(self, request):
        imgfile = os.path.join(settings.IMAGES_DIR, "background.png")
        return FileResponse(open(imgfile, 'rb'), content_type='image/*')
