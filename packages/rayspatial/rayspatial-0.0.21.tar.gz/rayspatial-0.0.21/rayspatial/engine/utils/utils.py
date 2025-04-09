# !/usr/bin/env python
# -*- coding: utf-8 -*-

def find_bbox_and_calculate_center(data):
    """
    在字典及其所有子字典中查找是否存在'bbox'键，如果找到则计算并返回中心点坐标。

    :param data: 需要搜索的字典
    :return: 如果找到'bbox'键，则返回中心点坐标(tuple)，否则返回None
    """
    if isinstance(data, dict):
        if 'bbox' in data:
            bbox = data['bbox']
            # bbox格式为 [min_lon, min_lat, max_lon, max_lat]
            center_lon = (bbox[0] + bbox[2]) / 2
            center_lat = (bbox[1] + bbox[3]) / 2
            return center_lat, center_lon
        for value in data.values():
            result = find_bbox_and_calculate_center(value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_bbox_and_calculate_center(item)
            if result is not None:
                return result
    return None
