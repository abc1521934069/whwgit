# -*- coding=utf-8 -*-

import os
from io import BytesIO
import json
from django.views import View
from django.http import JsonResponse, HttpResponse
import hashlib
from utils.response import CommonResponseMixin
from Project import settings
from apis.models import Article, Image, File
from authorization.models import UserInfo
from utils.response import ReturnCode
import PIL.Image
from django.http import FileResponse


class ResourceArticleView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        try:
            Article.objects.filter()[0]
        except:
            judge_exists = False
        if judge_exists:
            articles = []
            temp_articles = Article.objects.filter().order_by("-time")
            for article in temp_articles:
                articles.append({
                    "id": article.article_id,
                    "title": article.title,
                    "message": article.message,
                    "time": article.time.strftime("%Y-%m-%d")
                })
        else:
            articles = False
        json_articles = json.dumps(articles)
        # 将生成的级联数据返回
        response_data.append(json_articles)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        article_data = received_body.get('data')
        # 修改/发布文章
        user = UserInfo.objects.filter(user_id=article_data.get("user_id"))[0]
        article_id = article_data.get("article_id")
        if article_id == '':
            Article.objects.create(
                title=article_data.get("title"),
                message=article_data.get("message"),
                user=user
            )
            message = 'add article successfully.'
        else:
            article = Article.objects.filter(article_id=article_id)[0]
            article.title = article_data.get("title")
            article.message = article_data.get("message")
            article.editor = user
            article.save()
            message = 'update article successfully.'
        # 操作完成
        response = self.wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class ResourceImageView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        try:
            Image.objects.filter()[0]
        except:
            judge_exists = False
        if judge_exists:
            images = []
            temp_images = Image.objects.filter().order_by("-time")
            for image in temp_images:
                images.append({
                    "id": image.image_id,
                    "name": image.name
                })
        else:
            images = False
        json_images = json.dumps(images)
        # 将生成的级联数据返回
        response_data.append(json_images)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        # 获取用户信息
        user_id = request.POST.get('user_id')
        user = UserInfo.objects.filter(user_id=user_id)[0]
        files = request.FILES
        response_data = []
        for key, uploaded_file in files.items():
            # 获取后缀名
            postfix_arr = str(uploaded_file).split('.')
            postfix = postfix_arr[len(postfix_arr) - 1]
            # 获取并新建图片
            content = uploaded_file.read()
            image_name = hashlib.md5(content).hexdigest() + '.' + postfix
            path = os.path.join(settings.IMAGES_DIR, image_name)
            f = open(path, 'wb+')
            f.write(content)
            f.close()
            if Image.objects.filter(name=image_name).count() == 0:
                image = Image.objects.create(
                    name=image_name,
                    user=user
                )
                response_data.append({
                    "id": image.image_id,
                    "name": image.name
                })
        response = self.wrap_json_response(data=response_data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


class CompressImageView(View, CommonResponseMixin):
    def get(self, request):
        id = request.GET.get('id')
        name = Image.objects.filter(image_id=id)[0].name
        imgfile = os.path.join(settings.IMAGES_DIR, name)
        if os.path.exists(imgfile):
            image = PIL.Image.open(imgfile)
            width = image.width
            height = image.height
            rate = 0.3  # 压缩率
            width = int(width * rate)  # 新的宽
            height = int(height * rate)  # 新的高
            # 生成缩略图
            image.thumbnail((width, height), PIL.Image.ANTIALIAS)
            # 将图片保存到内存中
            image_catch = BytesIO()
            image.save(image_catch, 'jpeg')
            # 从内存中取出bytes类型的图片
            data = image_catch.getvalue()
            return HttpResponse(data, content_type='image/*')
        else:
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_FOUND)
            return JsonResponse(data=response, safe=False)


class OriginalImageView(View, CommonResponseMixin):
    def get(self, request):
        id = request.GET.get('id')
        name = Image.objects.filter(image_id=id)[0].name
        imgfile = os.path.join(settings.IMAGES_DIR, name)
        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            return FileResponse(open(imgfile, 'rb'), content_type='image/*')
        else:
            response = self.wrap_json_response(code=ReturnCode.RESOURCE_NOT_FOUND)
            return JsonResponse(data=response, safe=False)



class ResourceFileView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        judge_exists = True
        try:
            File.objects.filter()[0]
        except:
            judge_exists = False
        if judge_exists:
            files = []
            temp_files = File.objects.filter().order_by("-time")
            for file in temp_files:
                files.append({
                    "id": file.file_id,
                    "name": file.name
                })
        else:
            files = False
        json_files = json.dumps(files)
        # 将生成的级联数据返回
        response_data.append(json_files)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        # 获取用户信息
        user_id = request.POST.get('user_id')
        user = UserInfo.objects.filter(user_id=user_id)[0]
        files = request.FILES
        response_data = []
        for key, uploaded_file in files.items():
            a=1
            # 获取并新建图片
            content = uploaded_file.read()
            path = os.path.join(settings.DOCUMENTS_DIR, key)
            f = open(path, 'wb+')
            f.write(content)
            f.close()
            if File.objects.filter(name=key).count() == 0:
                file = File.objects.create(
                    name=key,
                    user=user
                )
                response_data.append({
                    "id": file.file_id,
                    "name": file.name
                })
        response = self.wrap_json_response(data=response_data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


class DownloadFileView(View, CommonResponseMixin):
    def get(self, request):
        id = request.GET.get('id')
        name = File.objects.filter(file_id=id)[0].name
        data = open(settings.DOCUMENTS_DIR + name, 'rb')
        response = FileResponse(data)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="models.py"'
        return response
