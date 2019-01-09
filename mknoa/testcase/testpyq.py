# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import datetime

dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time_unix = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
sign_not_md5 = "inventory.query" + "04802e534b58e80ed80b69aef660c1a7" + "partnerkey" + "bef58a29b7d69b26b61356bdf5818a48" + "token" + "7bd0cb66421e297d0b31f9c6537cd809" + "ts" + "{0}".format(
    time_unix) + "bef58a29b7d69b26b61356bdf5818a48"
hash = hashlib.md5(sign_not_md5.encode("utf-8"))
sign = hash.hexdigest()
url = "http://open.erp321.com/api/open/query.aspx?partnerid={0}&partnerkey={1}&token={2}&ts={3}&method={4}&sign={5}" \
    .format("04802e534b58e80ed80b69aef660c1a7", "bef58a29b7d69b26b61356bdf5818a48",
            "7bd0cb66421e297d0b31f9c6537cd809", time_unix, "inventory.query", sign)

data = {
    "page_index": 1,
    "page_size": 30,
    "modified_begin": "2019-01-07 00:00:00",
    "modified_end": "2019-01-09 00:00:00",
    "sku_ids": "D418M0803"
}
f = requests.post(url, json=data)
print(f.text)