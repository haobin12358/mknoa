from flask import request, current_app
import os, uuid
from mknoa.service.SProducts import SProducts
from mknoa.service.SUsers import SUsers
from mknoa.common.error_response import TokenError, ParamsError
from mknoa.common.due_power import user_can_use
from mknoa.common.get_model_return_list import get_model_return_list

class CCommon(SProducts, SUsers):

    def upload_files(self):
        formdata = request.form
        files = request.files.get("file")
        if "FileType" not in formdata:
            return
        import platform
        from mknoa.config import Inforcode
        if platform.system() == "Windows":
            rootdir = Inforcode.WindowsRoot + formdata.get("FileType") + "/"
        else:
            rootdir = Inforcode.LinuxRoot + Inforcode.LinuxImgs + formdata.get("FileType") + "/"
        if not os.path.isdir(rootdir):
            os.makedirs(rootdir)

        filessuffix = str(files.filename).split(".")[-1]
        index = formdata.get("index", 1)
        jpg_uuid = str(uuid.uuid1())
        filename = formdata.get("FileType") + str(index) + jpg_uuid + "." + filessuffix
        filepath = os.path.join(rootdir, filename)
        print(filepath)
        files.save(filepath)
        response = {
            "status": 200,
            "message": "上传成功"
        }
        url = Inforcode.ip + Inforcode.LinuxImgs + formdata.get("FileType") + "/" + filename
        print(url)
        response["data"] = {}
        response["data"]["url"] = url
        response["data"]["filename"] = files.filename
        return response

    def get_product_list(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        if "page_num" not in args or "page_size" not in args:
            return ParamsError("参数异常，请检查page_size和page_num")
        if "sku_id" not in args or args["sku_id"] == "":
            args["sku_id"] = None
        if "brand" not in args or args["brand"] == "":
            args["brand"] = None
        if "i_name" not in args or args["i_name"] == "":
            args["i_name"] = None
        if "supplier_name" not in args or args["supplier_name"] == "":
            args["supplier_name"] = None
        power_tree = user_can_use(args["token"], "notice")
        user_id = power_tree["user_id"]
        if user_id != "1":
            tag_list = power_tree["tag_list"]
            product_list = []
            page_total = 0
            for tag in tag_list:
                if tag["tag_sn"]:
                    product_list = self.get_product_by_page(int(args["page_size"]), int(args["page_num"]),
                                                            tag["tag_sn"], args["sku_id"], args["brand"], args["i_name"],
                                                            args["supplier_name"])
                    page_total = len(self.get_product_by_page_count(tag["tag_sn"], args["sku_id"], args["brand"],
                                                                    args["i_name"], args["supplier_name"]))
        else:
            product_list = get_model_return_list(self.get_product_by_page(int(args["page_size"]), int(args["page_num"]),
                                                                          None,
                                                                                                      args["sku_id"],
                                                                                                      args["brand"],
                                                                                                      args["i_name"],
                                                                                                      args["supplier_name"]))
            page_total = len(get_model_return_list(self.get_product_by_page_count(None, args["sku_id"], args["brand"],
                                                                                  args["i_name"], args["supplier_name"])))

        for row in product_list:
            row["qty"] = 0
        page_count = int(page_total / int(args["page_size"])) + 1
        return {
            "status": 200,
            "message": "获取商品列表成功",
            "total_page": page_count,
            "total_count": page_total,
            "data": product_list
        }

    def get_qyt_list(self):
        args = request.args.to_dict()
        if "token" not in args:
            return TokenError("未登录")
        if "page_num" not in args or "page_size" not in args:
            return ParamsError("参数异常，请检查page_size和page_num")

        return {
            "data":[{
                "sku_id":"123456",
                "sale_num": 100
            }],
            "total_page":1,
            "total_count":1,
            "status":200,
            "message": "获取实时销售量成功"
        }

    def get_file(self):
        args = request.args.to_dict()

        from mknoa.config import Inforcode
        rootpath = Inforcode.LinuxFilePath
        if "token" not in args:
            return TokenError("未登录")

        if "url" not in args:
            return ParamsError("参数缺失")

        if "FileType" not in args:
            return ParamsError("文件类型缺失")
        # if not os.path.isdir(rootdir):
        url = args.get("url")
        url = url.split("/")
        filename = url[len(url) - 1]
        rootpath = os.path.join(rootpath, args["FileType"])
        filepath = os.path.join(rootpath, filename)
        current_app.logger.info("filepath:" + str(filepath))
        from flask import send_from_directory
        return send_from_directory(rootpath, filename, as_attachment=True)