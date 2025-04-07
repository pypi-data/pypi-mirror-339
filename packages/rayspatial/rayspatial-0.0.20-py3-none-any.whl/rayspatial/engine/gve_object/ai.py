# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial.engine.function_node import FunctionNode
from rayspatial.engine.function_helper import FunctionHelper
from typing import Union
from rayspatial import engine


class AI(FunctionNode):
    @staticmethod
    def building_extraction(image: dict):
        data = {
            "image": image
        }
        fun_node = FunctionHelper.apply(
            "/ai/services/buildingExtraction", "engine.AI", data
        )
        return fun_node

