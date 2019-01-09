# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
import mknoa.models.products as models

# 装饰器，用来解析数据库获取的内容，将获取到的对象转置为dict，将获取到的单个数据的tuple里的数据解析出来
def trans_params(func):
    def inner(*args, **kwargs):
        params = func(*args, **kwargs)
        result = []
        if params:
            for param in params:
                if isinstance(param, (list, tuple)):
                    data = param[0]
                    result.append(data)
                elif isinstance(param, models.Base):
                    param_dict = param.__dict__
                    for param_key in param_dict:
                        # 所有的model的dict里都有这个不需要的参数，所以删除掉
                        if param_key == "_sa_instance_state":
                            continue
                    result.append(param_dict)
                else:
                    result = params
        return result

    return inner


def add_model(model_name, **kwargs):
    print(model_name)
    if not getattr(models, model_name):
        print("model name = {0} error ".format(model_name))
        return
    model_bean = eval(" models.{0}()".format(model_name))
    for key in model_bean.__table__.columns.keys():
        if key in kwargs:
            setattr(model_bean, key, kwargs.get(key))
    from mknoa.service.DBSession import get_session
    session, status = get_session()
    if status:
        session.add(model_bean)
        session.commit()
        session.close()
        return True
    raise Exception("session connect error")
