# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from utils.response import CommonResponseMixin
from authorization.models import UserInfo, Course, UserPower
from utils.response import wrap_json_response, ReturnCode


class CourseView(View, CommonResponseMixin):
    def post(self, request):
        response_data = []
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        personal_data = received_body.get('data')
        # 获取用户课表
        judge_exists = True
        user = UserInfo.objects.filter(user_id=personal_data.get("user_id"))[0]
        try:
            user.course
        except:
            judge_exists = False
        if judge_exists:
            courses = []
            course = Course.objects.values().filter(user=user)[0]
            day = ["mon", "tue", "wed", "thu", "fri"]
            for i in range(1, 6):
                for j in range(1, 6):
                    column = day[j-1] + str(i)
                    courses.append({
                        "judge": True,
                        "tag": i * 10 + j,
                        "select": list(map(int, course.get(column)[1:-1].split(',')))
                    })
        else:
            courses = False
        json_courses = json.dumps(courses)
        # 将生成的级联数据返回
        response_data.append(json_courses)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)


class CourseEditView(View, CommonResponseMixin):
    def post(self, request):
        # 获取传送过来的数据
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        # 引号为传输时的变量名
        edit_data = received_body.get('data')
        courses = edit_data.get("courses")
        # 获取用户
        user = UserInfo.objects.filter(user_id=edit_data.get("user_id"))[0]
        try:
            course = Course.objects.filter(user=user)[0]
        except:
            course = Course(user=user)
        course.mon1 = str(courses[0]['select'])
        course.mon2 = str(courses[5]['select'])
        course.mon3 = str(courses[10]['select'])
        course.mon4 = str(courses[15]['select'])
        course.mon5 = str(courses[20]['select'])

        course.tue1 = str(courses[1]['select'])
        course.tue2 = str(courses[6]['select'])
        course.tue3 = str(courses[11]['select'])
        course.tue4 = str(courses[16]['select'])
        course.tue5 = str(courses[21]['select'])

        course.wed1 = str(courses[2]['select'])
        course.wed2 = str(courses[7]['select'])
        course.wed3 = str(courses[12]['select'])
        course.wed4 = str(courses[17]['select'])
        course.wed5 = str(courses[22]['select'])

        course.thu1 = str(courses[3]['select'])
        course.thu2 = str(courses[8]['select'])
        course.thu3 = str(courses[13]['select'])
        course.thu4 = str(courses[18]['select'])
        course.thu5 = str(courses[23]['select'])

        course.fri1 = str(courses[4]['select'])
        course.fri2 = str(courses[9]['select'])
        course.fri3 = str(courses[14]['select'])
        course.fri4 = str(courses[19]['select'])
        course.fri5 = str(courses[24]['select'])

        course.save()

        # 操作完成
        message = 'edit the course successfully.'
        response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)
