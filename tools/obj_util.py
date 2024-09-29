"""
@file: obj_util.py
@time: 2023/11/21 17:17
@desc:
"""


def dict_to_obj(model, dict_data):
    """
    将dict转换为obj
    :param model:
    :param dict_data:
    :return:
    """
    if model.model_pks.get(model.__name__.strip(), "_id") != "_id":
        dict_data[model.model_pks.get(model.__name__.strip(), "_id")] = dict_data["_id"]
        del dict_data["_id"]
    obj = model(**dict_data)
    return obj
