import random

import requests
from django.core.cache import cache

from swiper import config
from common import keys
from swiper.settings import DEBUG
from worker import celery_app


def gen_vcode(size=4):
    # 返回4位随机数(1000,9999)
    start = 10 ** (size - 1)
    end = 10 ** size - 1
    return random.randint(start, end)


@celery_app.task
def send_sms(phone):
    data = config.YZX_SMS_PARAMS.copy()
    vcode = gen_vcode()
    # 将vcode存入缓存中,VCODE-13311206665
    print(vcode)
    key = keys.VCODE % phone
    timeout = 86400 if DEBUG else 900
    cache.set(key, vcode, timeout=timeout)
    data["param"] = vcode
    data["mobile"] = phone
    # response = requests.post(config.YZX_SMS_API, json=data)
    # if response.status_code != 200:
    #     return False
    return True
