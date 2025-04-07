# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial.engine.serialize.serializer import serializer
import rayspatial.serve
from rayspatial.engine.utils.utils import find_bbox_and_calculate_center

class InteractiveSession(object):
    @staticmethod
    def get_md5_data(data):
        import hashlib
        return hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def getInfo(obj):
        chain = serializer(obj)
        headers = {"method": "test"}
        # rayspatial.serve.RsEngine.start()
        chain_res = rayspatial.serve.ServeExecute.execute(chain, headers)
        if chain_res.get("properties"):
            if chain_res.get("properties").get("bbox"):
                bbox = chain_res.get("properties").get("bbox")
                chain_res["center"] = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        elif find_bbox_and_calculate_center(chain):
            chain_res["center"] = find_bbox_and_calculate_center(chain)
        return chain_res
