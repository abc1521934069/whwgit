# -*- coding=utf-8 -*-

from django.urls import path

from apis.views import job, activity, resource, count, comment, record, listener

urlpatterns = [
    path(r'job', job.JobView.as_view(), name='job'),
    path(r'activity', activity.ActivityView.as_view(), name='activity'),
    path(r'addActivity', activity.AddActivityView.as_view(), name='addActivity'),
    path(r'activityPage', activity.ActivityPageView.as_view(), name='activityPage'),
    path(r'addActivityArrange', activity.AddArrangeView.as_view(), name='addActivityArrange'),
    path(r'addActivityMaterial', activity.AddMaterialView.as_view(), name='addActivityMaterial'),
    path(r'editActivityBasic', activity.EditBasicView.as_view(), name='editActivityBasic'),
    path(r'editActivityMessage', activity.EditMessageView.as_view(), name='editActivityMessage'),
    path(r'editActivityArrange', activity.EditArrangeView.as_view(), name='editActivityArrange'),
    path(r'editActivityMaterial', activity.EditMaterialView.as_view(), name='editActivityMaterial'),
    path(r'finishActivityArrange', activity.FinishActivityArrangeView.as_view(), name='finishActivityArrange'),
    path(r'finishActivityMaterial', activity.FinishActivityMaterialView.as_view(), name='finishActivityMaterial'),
    path(r'resourceArticle', resource.ResourceArticleView.as_view(), name='resourceArticle'),
    path(r'resourceImage', resource.ResourceImageView.as_view(), name='resourceImage'),
    path(r'compressImage', resource.CompressImageView.as_view(), name='compressImage'),
    path(r'originalImage', resource.OriginalImageView.as_view(), name='originalImage'),
    path(r'resourceFile', resource.ResourceFileView.as_view(), name='resourceFile'),
    path(r'downloadFile', resource.DownloadFileView.as_view(), name='downloadFile'),
    path(r'count', count.CountView.as_view(), name='count'),
    path(r'comment', comment.CommentView.as_view(), name='comment'),
    path(r'record', record.RecordView.as_view(), name='record'),
    path(r'activityListener', listener.ActivityListenerView.as_view(), name='activityListener'),
    path(r'recordListener', listener.RecordListenerView.as_view(), name='recordListener')
]