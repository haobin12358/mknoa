# -*- coding: utf-8 -*-
import json
import requests
import time
import hashlib
import datetime
from mknoa.common.base_service import db_session
from mknoa.models.products import Products
from mknoa.common.TransformToList import add_model
from mknoa.common.get_model_return_list import get_model_return_dict
time_start = datetime.datetime(2018, 11, 22, 0, 0, 0)
time_end = datetime.datetime(2018, 11, 29, 0, 0, 0)
while time_start < datetime.datetime(2018, 12, 20, 0, 0, 0):
    i = 1
    while True:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_unix = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
        sign_not_md5 = "sku.query" + "04802e534b58e80ed80b69aef660c1a7" + "partnerkey" + "bef58a29b7d69b26b61356bdf5818a48" + "token" + "7bd0cb66421e297d0b31f9c6537cd809" + "ts" + "{0}".format(
            time_unix) + "bef58a29b7d69b26b61356bdf5818a48"
        hash = hashlib.md5(sign_not_md5.encode("utf-8"))
        sign = hash.hexdigest()
        url = "http://open.erp321.com/api/open/query.aspx?partnerid={0}&partnerkey={1}&token={2}&ts={3}&method={4}&sign={5}" \
            .format("04802e534b58e80ed80b69aef660c1a7", "bef58a29b7d69b26b61356bdf5818a48",
                    "7bd0cb66421e297d0b31f9c6537cd809", time_unix, "sku.query", sign)
        if time_start == datetime.datetime(2018, 6, 1, 0, 0, 0) and i == 1:
            i = 155
        data = {
            "page_index": i,
            "page_size": 30,
            "modified_begin": time_start.strftime("%Y-%m-%d %H:%M:%S"),
            "modified_end": time_end.strftime("%Y-%m-%d %H:%M:%S")
        }
        f = requests.post(url, json=data)
        json_data = json.loads(f.text)
        if "datas" in json_data.keys():
            datas = json_data["datas"]
            print(datas)
            if datas:
                for row in datas:
                    print(row["sku_id"])
                    session = db_session()
                    sku = get_model_return_dict(session.query(Products.sku_id).filter_by(sku_id=row["sku_id"]).first())
                    print(sku)
                    if "sku_id" not in sku.keys():
                        if not row["name"]:
                            row["name"] = " "
                        if not row["supplier_name"]:
                            row["supplier_name"] = " "
                        new_product = add_model("Products",
                                              **{
                                                  "sku_id": row["sku_id"],
                                                  "i_id": row["i_id"],
                                                  "i_name": row["name"],
                                                  "properties_value": row["properties_value"],
                                                  "supplier_id": str(row["supplier_id"]),
                                                  "supplier_name": row["supplier_name"],
                                                  "brand": row["brand"]
                                              })
                    session.close()
            else:
                break
            i = i + 1
        else:
            print(json_data)
    time_start = time_start + datetime.timedelta(days=7)
    time_end = time_end + datetime.timedelta(days=7)