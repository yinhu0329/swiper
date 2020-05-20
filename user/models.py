import datetime
from django.db import models

from libs.mixins import ModelMixin

SEX = (
    ('男', '男'),
    ('女', '女'),
)


class User(models.Model):
    '''用户模型'''

    phonenum = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=50, unique=True, verbose_name='昵称')
    gender = models.CharField(max_length=8, choices=SEX,
                              verbose_name='性别', default='男')
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(
        max_length=1024, verbose_name='个人形象的URL',
        default="http://qak32ffdx.bkt.clouddn.com/morentouxiang.jpg")
    location = models.CharField(
        max_length=16, verbose_name='常居地', default="北京")

    class Meta:
        db_table = "user"

    # 讲model profile变成user的属性
    @property
    def profile(self):
        self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def birthday(self):
        # 用出生年月日构造日期
        birthday = datetime.date(
            self.birth_year, self.birth_month, self.birth_day)
        return birthday

    @property
    def age(self):
        # 获取当前日期
        today = datetime.date.today()

        # 用出生年月日构造日期
        birthday = self.birthday
        age = (today - birthday).days // 365
        # 用当前日期 减去 出生日期 , 取日子 // 365
        return age

    def __str__(self):
        return f'<User {self.nickname} {self.phonenum}>'

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'age': self.age,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,

        }


class Profile(models.Model, ModelMixin):
    dating_location = models.CharField(max_length=128, verbose_name="目标城市")
    dating_gender = models.CharField(max_length=8, choices=SEX, verbose_name="匹配的性别")
    min_distance = models.IntegerField(default=0, verbose_name="最小查找范围")
    max_distance = models.IntegerField(default=50, verbose_name="最大查找范围")
    min_dating_age = models.IntegerField(default=18, verbose_name="最小交友年龄")
    max_dating_age = models.IntegerField(default=50, verbose_name="最大交友年龄")
    vibration = models.BooleanField(default=True, verbose_name="开启震动")
    only_matched = models.BooleanField(default=True, verbose_name="不让陌生人查看我的相册")
    auto_play = models.BooleanField(default=True, verbose_name="自动播")

    class Meta:
        db_table = 'profile'