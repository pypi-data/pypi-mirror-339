# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial import engine
from rayspatial.engine.function_node import FunctionNode
from rayspatial.engine.function_helper import FunctionHelper
from rayspatial.serve.core.error.gve_error import RSError, RSErrorCode


class Feature(FunctionNode):
    def __init__(self, geometry, properties=None):
        if isinstance(geometry, engine.Geometry):
            if properties is not None and not isinstance(properties, dict):
                raise RSError(
                    RSErrorCode.ARGS_ERROR,
                    f"properties only dict arguments are supported, passed as {type(properties)}",
                )
        data = {
            "geometry": geometry,
            "properties": properties,
        }
        super(Feature, self).__init__("Feature", data)
        self.updateStep("/feature", data, self)

    def getBound(self):
        data = self
        fun_node = FunctionHelper.apply("Feature.getBound", "engine.Feature", data)
        self.updateStep("/feature/getBound", data, fun_node)
        return fun_node

    def getCenter(self):
        bbox = self.getBound()
        if bbox is not None and isinstance(bbox, list):
            center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
            return center
        raise RSError(RSErrorCode.ARGS_ERROR, f"Failed to obtain the Center. bbox: {bbox}")

    def transform(self, proj: str):
        if proj is not None and not isinstance(proj, str):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"proj supports only str type arguments, passed in as {type(proj)}"
            )
        data = {
            "feature": self,
            "proj": proj
        }
        fun_node = FunctionHelper.apply("Feature.transform", "engine.Feature", data)
        self.updateStep("/feature/transform", data, fun_node)
        return fun_node

