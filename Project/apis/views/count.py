# -*- coding=utf-8 -*-

import json
from django.views import View
from django.http import JsonResponse
from apis.models import Resource
from authorization.models import Dept, UserClub, UserInfo, College, Register
from utils.response import CommonResponseMixin
from django.db.models import Count, Q


class CountView(View, CommonResponseMixin):
    def get(self, request):
        response_data = []
        count_date = []
        # 获取整体统计
        population_count = {
            "all": UserInfo.objects.filter(judge_invalid=True).count(),
            "boy": UserInfo.objects.filter(judge_invalid=True, sex=True).count(),
            "girl": UserInfo.objects.filter(judge_invalid=True, sex=False).count(),
        }
        count_date.append(population_count)
        # 获取部门统计
        dept_count = []
        temp_depts = Dept.objects.all()
        for dept in temp_depts:
            boy = 0
            girl = 0
            temp_clubs = UserClub.objects.filter(dept=dept)
            for club in temp_clubs:
                if club.user.judge_invalid:
                    if club.user.sex:
                        boy += 1
                    else:
                        girl += 1
            dept_count.append({
                "name": dept.name,
                "boy": boy,
                "girl": girl
            })
        count_date.append(dept_count)
        # 获取学院统计
        college_count = []
        temp_college = UserInfo.objects.exclude(judge_invalid=False).values("college").annotate(Count("user_id"))
        for college in temp_college:
            college_count.append({
                "name": College.objects.filter(college_id=college["college"])[0].name,
                "count": college["user_id__count"]
            })
        count_date.append(college_count)
        # 获取社团物资统计
        resource_count = []
        temp_resources = Resource.objects.all()
        for resource in temp_resources:
            resource_count.append({
                "name": resource.name,
                "count": resource.count
            })
        count_date.append(resource_count)
        # 获取报名总体统计
        boy = 0
        girl = 0
        temp_registers = Register.objects.all()
        for register in temp_registers:
            if register.user.sex:
                boy += 1
            else:
                girl += 1
        register_population_count = {
            "all": Register.objects.all().count(),
            "boy": boy,
            "girl": girl,
        }
        count_date.append(register_population_count)
        # 获取报名部门统计
        register_dept_count = []
        for dept in temp_depts:
            boy = 0
            girl = 0
            temp_registers = Register.objects.filter(Q(dept1=dept) | Q(dept2=dept))
            for register in temp_registers:
                if register.user.sex:
                    boy += 1
                else:
                    girl += 1
            register_dept_count.append({
                "name": dept.name,
                "boy": boy,
                "girl": girl
            })
        count_date.append(register_dept_count)
        # 获取报名学院统计
        register_college_count = []
        register_users = [register.user.user_id for register in Register.objects.all()]
        temp_register_college = UserInfo.objects.filter(user_id__in=register_users).values("college").annotate(Count("user_id"))
        for college in temp_register_college:
            register_college_count.append({
                "name": College.objects.filter(college_id=college["college"])[0].name,
                "count": college["user_id__count"]
            })
        count_date.append(register_college_count)
        # 将生成的级联数据返回
        json_count_date = json.dumps(count_date)
        response_data.append(json_count_date)
        response = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response, safe=False)
