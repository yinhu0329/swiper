import random

import requests
from django.core.cache import cache

# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import Com

from swiper import config
from common import keys


def gen_vcode(size=4):
    # 返回4位随机数(1000,9999)
    start = 10 ** (size - 1)
    end = 10**size - 1
    return random.randint(start, end)


def send_sms(phone):
    data = config.YZX_SMS_PARAMS.copy()
    vcode = gen_vcode()
    # 将vcode存入缓存中,VCODE-13311206665
    key = keys.VCODE % phone
    cache.set(key, vcode, timeout=180)
    data["param"] = vcode
    data["mobile"] = phone
    response = requests.post(config.YZX_SMS_API, json=data)
    if response.status_code != 200:
        return False
    return True


"""
client = AcsClient('LTAI4GJzjiZqBfp1NEshQvvU',
                   'wk5arWSaWX9bSCq0nBXHqh7vXcaeEw', 'cn-hangzhou')
def send_sms(phone):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', "18676689715")
    request.add_query_param('SignName', "swiper")
    request.add_query_param('TemplateCode', "SMS_189840981")
    request.add_query_param('TemplateParam', "{\"code\":\"1234\"}")

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
"""
