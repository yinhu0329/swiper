import re
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from libs.sms import send_sms
from common import errors, keys
from libs.http import render_json


def submit_phone(request):
    """获取短信验证码"""
    phone = request.POST.get('phone')

    # 验证手机号格式
    result = re.match(r'^1[3456789]\d{9}', phone)

    if not result:
        # return JsonResponse({'code': errors.PHONE_ERROR, 'data': '手机格式错误'})
        return render_json(code=errors.PHONE_ERROR, data='手机格式有误')

        # 发送验证码
    flag = send_sms(phone)
    if flag:
        # return JsonResponse({'code': 0, 'data': '手机验证码发送成功'})
        return render_json(data="手机验证码发送成功")
    else:
        # return JsonResponse({'code': errors.SEND_VCODE_ERROR, 'data': '手机验证码发送失败'})
        return render_json(code=errors.SEND_VCODE_ERROR, data='手机验证码发送失败')


def submit_vcode(request):
    """通过验证码登录注册
    用户提交收入短信验证码,接受之后,和刚才发送的短信验证码做对比
    如果正确,就可以登录注册,不正确,返回错误信息
    """
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    # 从缓存中获取vcode
    key = keys.VCODE % phone
    cache_vcode = cache.get(key)
    if vcode == cache_vcode:
        # 相同可以登录和注册
        pass
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    """查看个人交友资料"""
    pass


def edit_profile(request):
    """修改个人资料及交友资料"""
    pass


def upload_avatar(request):
    """头像上传"""
    pass
