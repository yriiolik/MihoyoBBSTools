import config
import tools
from loghelper import log
from request import http

# 需要注册后使用公益打码
# https://ocr.kuxi.tech/user/login
token = ''


def game_captcha(gt: str, challenge: str):
    response = geetest(gt, challenge, 'https://passport-api.mihoyo.com/account/ma-cn-passport/app/loginByPassword')
    # 失败返回None 成功返回validate
    if response is None:
        return response
    else:
        return response['validate']


def bbs_captcha(gt: str, challenge: str):
    response = geetest(gt, challenge,
                       "https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required=true&act_id"
                       "=e202009291139501&utm_source=bbs&utm_medium=mys&utm_campaign=icon")
    # 失败返回None 成功返回validate
    if response is None:
        return response
    else:
        return response['validate']


def geetest(gt: str, challenge: str, referer: str):
    response = http.post('http://api.rrocr.com/api/recognize.html', params={
        'appkey': config.config['captcha']['token'],
        'gt': gt,
        'challenge': challenge,
        'referer': referer
    }, timeout=60000)
    data = response.json()
    if data['status'] != 0:
        log.warning(data['msg'])  # 打码失败输出错误信息
        return None
    return data['data']  # 失败返回None 成功返回validate
