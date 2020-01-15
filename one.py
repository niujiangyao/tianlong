#!/usr/bin/python3
import requests
import time
import hashlib
import base64
import json
from config import *
header = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'Cookie': Cookie  # 用户登录状态sid
}
headercode = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'Content-type': 'application/x-www-form-urlencoded'
}

'''
collectdata = {
    'goods_id':6479429
}
collect = requests.post('http://tl.cyg.changyou.com/goods/favorgoods', data=collectdata, headers=header)
print(collect.text)
'''
def waiting():
    # dt = '2020-01-20 05:21:01'
    # timearray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # t = time.mktime(timearray)
    # print(timearray)
    # sec = str(int(t) - int(time.time()))
    # print(sec)
    sec = secs  # 剩余时间
    i = 0
    # time.sleep(sec)
    while i < 10:
        time.sleep(int(sec / 10))
        i += 1
        print('心跳第几次' + str(i))
    getcaptcha()


def getcaptcha():
    captcha = requests.get('http://tl.cyg.changyou.com/transaction/captcha-image',
                           params={'goods_serial_num': goods_serial_num}, headers=header)
    print(captcha.status_code)
    tm = str(int(time.time()))
    print(tm)
    testfunc(base64.b64encode(captcha.content))
    with open(tm + '.png', 'wb') as fd:
        fd.write(captcha.content)


def CalcSign(pd_id, passwd, timestamp):
    md5 = hashlib.md5()
    md5.update((timestamp + passwd).encode())
    csign = md5.hexdigest()

    md5 = hashlib.md5()
    md5.update((pd_id + timestamp + csign).encode())
    csign = md5.hexdigest()
    return csign


num = 0
def order(captcha):
    data = {
        'goods_serial_num': goods_serial_num,
        'captcha_code': captcha
    }
    res = requests.post('http://tl.cyg.changyou.com/transaction/buy', data=data, headers=header)
    print(res.text)
    global num
    while num < 5:
        if res.text == 'captcha_error':
            num += 1
            return getcaptcha()
        else:
            break


def testfunc(img):
    tm = str(int(time.time()))
    sign = CalcSign(account, password, tm)
    msg = {
        'user_id': account,  # 用户中心页可以查询到pd信息
        'timestamp': tm,
        'sign': sign,
        'img_data': img,
        'predict_type': '30400'
        }
    code = requests.post('http://pred.fateadm.com/api/capreg', data=msg, headers=headercode)
    print(code.text)
    a = json.loads(code.text)
    # print(a)
    # print(a['RetCode'])
    # print(a['RspData'])
    print(json.loads(a['RspData'])['result'])
    order(json.loads(a['RspData'])['result'])


if __name__ == "__main__":
    waiting()
