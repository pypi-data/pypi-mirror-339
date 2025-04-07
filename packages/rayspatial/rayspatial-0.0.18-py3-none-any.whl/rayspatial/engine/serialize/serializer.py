# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial import engine
import copy
from datetime import datetime


def get_return_libtype(data):
    last_data = data[-1]
    router_key = last_data['router'].split("/")
    if router_key[1] == "geometry" and len(router_key) > 2:
        last_data["resultLibType"] = router_key[2]
    elif router_key[1] == "geometry" and len(router_key) == 2:
        last_data["resultLibType"] = last_data["params"]["type"]
    elif router_key[1] == "ai":
        last_data["resultLibType"] = "FeatureCollection"
    elif last_data['router'] == "/image/BatchProcessing":
        last_data["resultLibType"] = "FeatureCollection"
    else:
        # Keep it the same except for the first letter, which is capitalized
        last_data["resultLibType"] = router_key[1][0].upper() + router_key[1][1:]
    return data


def serializer(obj):
    def replace_objects(data, params):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) or isinstance(value, list):
                    replace_objects(value, params)
                elif isinstance(value, (engine.gve_object.image.Image, engine.gve_object.geometry.Geometry)):
                    ref_num = list(value.params.values())[0]
                    data[key] = ref_num
        elif isinstance(data, list):
            for item in data:
                replace_objects(item, params)

    def insert_step_based_on_object_type(data_list):
        orig_data = copy.deepcopy(data_list)
        for item in data_list:
            for key, value in item['args'].items():
                handle_value(value, orig_data)

        return orig_data

    def handle_value(value, orig_data):
        # 检查值是否是 `Geometry` 或 `Image` 对象
        if isinstance(value, (engine.gve_object.image.Image, engine.gve_object.geometry.Geometry)):
            # 获取 step 属性并递归处理
            for step in value.step:
                handle_value(step['args'], orig_data)
                # 在列表中插入该 step 值
                orig_data.insert(-1, step)
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                handle_value(sub_value, orig_data)
        elif isinstance(value, list):
            for sub_value in value:
                handle_value(sub_value, orig_data)

    step = obj.step
    params = obj.params
    data = insert_step_based_on_object_type(step)

    replace_objects(data, params)
    updated_data = [{**{'router': d.pop('key'), 'params': d.pop('args'), 'order': d.pop('stepNum')}, **d} for d in
                    copy.deepcopy(data)]
    operatorArr = get_return_libtype(updated_data)
    chain = {
        "id": f'rs_execute_{datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[:-3]}',
        "executeObjectKey": "$executeObject",
        "executeObject": None,
        "operatorArr": operatorArr
    }
    return chain


