from flask import request
import os, uuid

class CCommon():

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