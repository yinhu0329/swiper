from django.db import models


class Swiped(models.Model):
    """可以把滑动的操作,抽象成一个模型
        用一个模型精准的表示用户的滑动操作即可
        一个滑动操作会有被滑人的id,滑动人的id,滑动的类型,滑动的时间点
    """
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike'),
    )

    uid = models.IntegerField(verbose_name='用户自身的id')
    sid = models.IntegerField(verbose_name='被滑动人的id')
    mark = models.CharField(choices=MARK, verbose_name='滑动类型', max_length=16)
    time = models.DateTimeField(verbose_name='滑动时间', auto_now_add=True)

    class Meta:
        db_table = "swiped"

    @classmethod
    def like(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='like')

    @classmethod
    def dislike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='dislike')

    @classmethod
    def superlike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='superlike')

    @classmethod
    def has_like(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, mark__in=['like', 'superlike']).exists()


class Friend(models.Model):
    # 一般多对多中间表就是关联表id
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    class Meta:
        db_table = "friend"

    @classmethod
    def make_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid2 > uid1 else (uid2, uid1)
        friendship = Friend.objects.create(uid1=uid1, uid2=uid2)
        return friendship

    @classmethod
    def delete_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid2 > uid1 else (uid2, uid1)
        return cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def is_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid2 > uid1 else (uid2, uid1)
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()
