import re
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from libs.sms import send_sms
from common import errors, keys
from libs.http import render_json
from user.models import User
from user.models import Profile
from user import forms
from libs.qiniuyun import upload_qiniu
from swiper import config


@require_http_methods(['POST'])
def submit_phone(request):
    """获取短信验证码"""
    phone = request.POST.get('phone')
    # 验证手机号格式
    result = re.match(r'^1[3456789]\d{9}', phone)

    if not result:
        return render_json(code=errors.PHONE_ERROR, data='手机格式有误')
    # 发送验证码
    flag = send_sms(phone)
    if flag:
        return render_json(data="手机验证码发送成功")
    else:
        return render_json(code=errors.SEND_VCODE_ERROR, data='手机验证码发送失败')


@require_http_methods(['POST'])
def submit_vcode(request):
    """通过验证码登录注册
    用户提交收入短信验证码,接受之后,和刚才发送的短信验证码做对比
    如果正确,就可以登录注册,不正确,返回错误信息
    """
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    # 从缓存中获取vcode
    key = keys.VCODE % phone
    cache_vcode = str(cache.get(key))
    if vcode and (vcode == cache_vcode):
        # 相同可以登录和注册
        # app的登录注册:如果是第一次登录那就注册一个新用户.
        # 使用get_or_create进行优化
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={"nickname": phone})
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    """查看个人交友资料"""
    uid = request.uid
    user = User.objects.get(id=uid)
    # 用户的交友资料和用户是一对一的关系, 怎么实现一对一的关系?
    # 保证两张表的id是一致. user id = 1, 对应的profile id 也是1.
    return render_json(data=user.profile.to_dict(exclude=(id,)))


def edit_profile(request):
    """修改个人资料及交友资料"""
    # 定义两个form表单的实例对象
    user_form = forms.UserFrom(request.POST)
    profile_form = forms.ProfileForm(request.POST)
    # 检查user_form和profile_from
    if not user_form.is_valid() or not profile_form.is_valid():
        form_errors = {}
        form_errors.update(user_form.errors)
        form_errors.update(profile_form.errors)
        return render_json(code=errors.PROFILE_ERROR, data=form_errors)
    uid = request.uid
    # user_form.cleaned_data本身就是一个字典,可以使用**进行解包
    User.objects.filter(id=uid).update(**user_form.cleaned_data)
    # 更新或者创建profile
    # 注意profile和user是一对一的关系,创建的profile的时候为了满足一对一的关系必须保证创建出来的profile的id和对应的user的id是一致的
    Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)
    return render_json()


def upload_avatar(request):
    """头像上传
        先获取用户上传的文件
        然后保存到本地
        然后上传到七牛云
        使用七牛云的图片地址更新用户的avatar属性
    """
    # 保存到本地,并重新命名文件
    avatar = request.FILES.get('avatar')
    # print(type(avatar))
    # print(avatar.name)
    # print(avatar.size)
    # print(avatar.content_type)
    uid = request.uid
    filename = keys.AVATAR % uid
    """
    将文件保存到本地,用put_file方法上传
    print(filename)
    with open(f'./media/{filename}', mode='wb+') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    # 上传到七牛云
    avatar =f'./media/{filename}'
    upload_qiniu(avatar, filename)
    print("------------********-----")

    """

    upload_qiniu(avatar.read(), filename)
    user = User.objects.get(id=uid)
    user.avatar = config.QN_URL + filename
    user.save()
    return render_json()
