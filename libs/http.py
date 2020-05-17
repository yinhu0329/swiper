
import json

from django.http import HttpResponse

from swiper.settings import DEBUG


def render_json(code=0, data=None):
    # 开发调试的时候,希望返回json是一种比较人性化的,格式化的json
    #  如果生产环境,希望json是压缩过的
    data_dict = {
        'code': code,
        'data': data
    }
    if DEBUG:
        # 说明是开发环境
        data_dump = json.dumps(data_dict, indent=4,
                               ensure_ascii=False, sort_keys=True)
    else:
        # 说明是生产环境
        data_dump = json.dumps(data_dict, indent=4,
                               ensure_ascii=False, separator=[':', ','])
    return HttpResponse(data_dump)
