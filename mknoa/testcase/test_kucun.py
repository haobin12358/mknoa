# -*- coding: utf-8 -*-
import json
import requests
import time
import hashlib
import datetime
from mknoa.common.base_service import db_session
from mknoa.models.products import ProductsQyt
from mknoa.common.TransformToList import add_model
from mknoa.common.get_model_return_list import get_model_return_dict
time_start = datetime.datetime(2019, 1, 4, 0, 0, 0)
time_end = datetime.datetime(2019, 1, 5, 0, 0, 0)
while time_start > datetime.datetime(2018, 12, 10, 0, 0, 0):
    i = 1
    while True:
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
            "page_index": i,
            "page_size": 50,
            "modified_begin": time_start.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_end": time_end.strftime("%Y-%m-%d %H:%M:%S")
        }
        f = requests.post(url, json=data)
        json_data = json.loads(f.text)
        if "inventorys" in json_data.keys():
            datas = json_data["inventorys"]
            print(datas)
            if datas:
                for row in datas:
                    print(row["sku_id"])
                    session = db_session()
                    sku = get_model_return_dict(session.query(ProductsQyt.sku_id).filter_by(sku_id=row["sku_id"]).first())
                    print(sku)
                    if "sku_id" not in sku.keys():
                        new_product = add_model("ProductsQyt",
                                              **{
                                                  "sku_id": row["sku_id"],
                                                  "qty": row["qty"],
                                                  "order_lock": row["order_lock"]
                                              })
                    session.close()
            else:
                break
            i = i + 1
        else:
            print(json_data)
    time_start = time_start + datetime.timedelta(days=-1)
    time_end = time_end + datetime.timedelta(days=-1)