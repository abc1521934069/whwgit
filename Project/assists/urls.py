# -*- coding=utf-8 -*-

from django.urls import path

from assists.views import indexInfo, image, specialPower


urlpatterns = [
    path(r'indexInfo', indexInfo.IndexInfoView.as_view(), name='indexInfo'),
    path(r'image', image.ImageView.as_view(), name='image'),
    path(r'specialPower', specialPower.SpecialPowerView.as_view(), name='specialPower')
]