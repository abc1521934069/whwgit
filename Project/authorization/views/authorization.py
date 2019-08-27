# -*- coding=utf-8 -*-

import json
from django.http import JsonResponse
from utils.response import wrap_json_response, ReturnCode
from utils.auth import c2s, AccountInfo
from authorization.models import UserInfo, UserClub, Register
from assists.models import Master


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权

    post_data = {
        'encryptedData': 'xxxx',
        'appId': 'xxx',
        'sessionKey': 'xxx',
        'iv': 'xxx'
    }
    '''
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    app_id = post_data.get('appId').strip()
    code = post_data.get('code').strip()
    if not (app_id and code):
        response['result_code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        data = c2s(app_id, code)
    except Exception as e:
        response['result_code'] = ReturnCode.FAILED
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    open_id = data.get('openid')
    if not open_id:
        response['result_code'] = ReturnCode.FAILED
        response['message'] = 'authorization error.'
        return JsonResponse(response, safe=False)
    request.session['open_id'] = open_id
    request.session['is_authorized'] = True

    # User.objects.get(open_id=open_id) # 不要用get，用get查询如果结果数量 !=1 就会抛异常
    # 如果用户不存在，则新建用户
    if not UserInfo.objects.filter(openid=open_id):
        new_user = UserInfo(openid=open_id)
        new_user.save()

    user = UserInfo.objects.filter(openid=open_id)[0]
    user_id = user.user_id
    account_info = AccountInfo(id=user_id)

    if (not Register.objects.filter(user=user_id)) and (not UserClub.objects.filter(user=user_id)):
        account_info.set_status(register=False, status=False)
    else:
        account_info.set_status(register=True, status=user.judge_invalid)

    if user.judge_invalid:
        account_info.set_power(user.userpower)
        account_info.set_position(user.userclub)
        account_info.set_global(Master.objects.all()[0])

    # 自定义类对象转换成json对象   普通对象直接用 json.dumps(object_name) 即可
    json_account_info = json.dumps(account_info.__dict__, ensure_ascii=False)
    message = 'user authorize successfully.'
    response = wrap_json_response(data=json_account_info, code=ReturnCode.SUCCESS, message=message)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)
