from django.db.models import Q

from common import errors
from libs.http import render_json
from social import logics
from social.models import Friend
from user.models import User


def get_recd_list(request):
    data = logics.get_recd_list(request.uid)
    return render_json(data=data)


def like(request):
    uid = request.uid
    sid = int(request.GET.get('sid'))
    flag = logics.like(uid, sid)
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


def dislike(request):
    # 创建一条mark为不喜欢的
    uid = request.uid
    sid = int(request.GET.get('sid'))
    logics.dislike(uid, sid)
    return render_json()


def superlike(request):
    uid = request.uid
    sid = int(request.GET.get('sid'))
    flag = logics.superlike(uid, sid)
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


def rewind(request):
    """:argument
        反悔功能,
        只能反悔上一次的滑动
        其实反悔就是把最后一条Swiper记录删除
        一天只能3次反悔次数,反悔的次数可以记录到redis中
    """
    uid = request.uid
    if logics.rewind(uid):
        return render_json()


def show_friends(request):
    # 从Friend表中查出uid 是当前登录用户的id,或者sid是当前登录用户的id
    uid = request.uid
    data = logics.show_friends(uid)
    return render_json(data=data)
