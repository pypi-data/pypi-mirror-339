# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial import engine
from .function_node import FunctionNode


class FunctionHelper(object):
    @classmethod
    def cast(cls, node, kclass):
        if kclass == "engine.Image":
            node.__class__ = engine.Image
        # elif kclass == "engine.AI":
        #     node.__class__ = engine.AI
        elif kclass == "engine.Geometry":
            node.__class__ = engine.Geometry
        # elif kclass == "engine.Feature":
        #     node.__class__ = engine.Feature
        # elif kclass == "engine.ImageCollection":
        #     node.__class__ = engine.ImageCollection
        # elif kclass == "engine.FeatureCollection":
        #     node.__class__ = engine.FeatureCollection
        elif kclass in ("int", "float", "bool", "str", "list", "tuple", "dict", "object"):
            pass
        return node

    @classmethod
    def apply(cls, name, returns, args):
        node = FunctionNode(name, args)
        node.updateStep(name, args, node)
        return cls.cast(node, returns)
