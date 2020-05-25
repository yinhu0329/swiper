import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys, errors
from social.models import Swiped, Friend
from swiper import config
from user.models import User


def get_recd_list(uid):
    user = User.objects.get(id=uid)
    # 当前年份
    curr_year = datetime.date.today().year
    # 最小匹配年龄
    min_age = user.profile.min_dating_age
    # 最大匹配年龄
    max_age = user.profile.max_dating_age
    # 匹配目标城市
    dating_location = user.profile.dating_location
    # 最小的匹配年份
    min_birth_year = curr_year - max_age
    # 最大的匹配年份
    max_birth_year = curr_year - min_age
    # 匹配的性别
    dating_gender = user.profile.dating_gender
    """
    从swiped表中查询已经被当前用户滑过的人.
    已经滑过的人不要出现在推荐列表了,
    只需要被滑过人的id
    """
    swiped_list = Swiped.objects.filter(uid=uid).only('sid')
    # 取出sid
    sid_list = [s.sid for s in swiped_list]
    # 把自己排除
    sid_list.append(uid)
    users = User.objects.filter(location=dating_location, birth_year__range=[min_birth_year, max_birth_year],
                                gender=dating_gender).exclude(
        id__in=sid_list)[:20]
    data = [user.to_dict() for user in users]
    return data


def like(uid, sid):
    Swiped.like(uid, sid)
    if Swiped.has_like(uid=sid, sid=uid):
        Friend.make_friend(uid, sid)
        return True
    return False


def dislike(uid, sid):
    Swiped.dislike(uid, sid)
    # 删除好友记录
    Friend.delete_friend(uid, sid)


def superlike(uid, sid):
    Swiped.superlike(uid, sid)
    if Swiped.has_like(uid=sid, sid=uid):
        Friend.make_friend(uid, sid)
        return True
    return False


def rewind(uid):
    key = keys.REWIND % uid
    cached_rewind_times = cache.get(key, 0)
    if cached_rewind_times < config.MAX_REWIND_TIMES:
        # 说明可以执行反悔操作,查找上一次执行的swiped记录
        record = Swiped.objects.latest('time')
        # 如果建立了好友关系,好友关系也需要取消
        sid = record.sid

        if Friend.is_friend(uid, sid):
            Friend.delete_friend(uid, sid)
        record.delete()
        #         更新缓存
        cached_rewind_times += 1
        now = datetime.datetime.now()
        timeout = 86400 - (3600 * now.hour + 60 * now.minute + now.second)
        cache.set(key, cached_rewind_times, timeout=timeout)
        return True
    else:
        raise errors.ExceedMaximumRewindTimes


def show_friends(uid):
    friends = Friend.objects.filter(Q(uid1=uid) | Q(uid2=uid))
    friends_id = []
    for friend in friends:
        if friend.uid1 == uid:
            friends_id.append(friend.uid2)
        else:
            friends_id.append(friend.uid1)

    users = User.objects.filter(id__in=friends_id)
    # 下面这种写法,每次循环都会访问一次数据库
    # users = []
    # for id in friends_id:
    #     user = User.objects.get(id=id)
    #     users.append(user)
    data = [user.to_dict() for user in users]
    return data
