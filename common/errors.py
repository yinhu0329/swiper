"""所有的错误码放在这里"""

PHONE_ERROR = 1000
SEND_VCODE_ERROR = 1001
VCODE_ERROR = 1002
PROFILE_ERROR = 1003
LOGIN_REQUIRED = 1004
EXCEED_MAXIMUM_REWIND_TIMES = 1005


class LogicErr(Exception):
    code = None
    data = None


def gen_logic_err(name, code, data):
    return type(name, (LogicErr,), {'code': code, 'data': data})


PhoneError = gen_logic_err('PhoneError', code=1000, data='手机号码格式错误')
SendVcodeError = gen_logic_err('SendVcodeError', code=1001, data='发送手机验证码错误')
VcodeError = gen_logic_err('VcodeError', code=1002, data='短信验证码错误')
ProfileError = gen_logic_err('ProfileError', code=1003, data='个人交友资料错误')
LoginRequired = gen_logic_err('LoginRequired', code=1004, data='请登录')
ExceedMaximumRewindTimes = gen_logic_err('ExceedMaximumRewindTimes', code=1005, data='超过当日最大反悔次数')
PermissonDenied = gen_logic_err('PermissonDenied', code=1006, data='权限不足,请充值')
