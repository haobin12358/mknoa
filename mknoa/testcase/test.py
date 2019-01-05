# -*- coding: utf-8 -*-
import json
import requests
import time
import hashlib
random = 104556
url = "https://live.kewail.com/sms/v1/sendsinglesms?accesskey={0}&random={1}".format("5c2dfc6c87b65f2bc9a0fe4f", random)
print(url)
dt = "2019-01-03 20:29:29"
time_unix = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
print(time_unix)
print(type(time_unix))
sig_not_sha = "secretkey={0}&random={1}&time={2}&mobile={3}".format("235d8ad1b70a42298e55b5688b7f7c9d", random, str(time_unix), "17706441101")
hash = hashlib.sha256()
hash.update(sig_not_sha.encode("utf-8"))
sig = hash.hexdigest()
print(sig)
data = {
    "tel": {
        "nationcode": "86",
        "mobile": "17706441101"
    },
    "type": 0,
    "msg": "【hindigo】您的验证码：123456，非常重要，请勿泄漏。",
    "sig": sig,
    "time": time_unix,
    "extend": "",
    "ext": ""
}
print(data)
f = requests.post(url, json=data)

print(f.text)
