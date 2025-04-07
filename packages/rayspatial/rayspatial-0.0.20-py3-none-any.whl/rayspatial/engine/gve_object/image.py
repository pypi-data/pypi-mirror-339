# !/usr/bin/env python
# -*- coding: utf-8 -*-

from rayspatial.engine.function_node import FunctionNode
from rayspatial.engine.function_helper import FunctionHelper
from rayspatial.serve.core.error.gve_error import RSError, RSErrorCode
import rayspatial.engine as engine
from typing import Union


class Image(FunctionNode):
    def __init__(self, args=None):
        self.resp = None
        data = {"constant": args}
        super(Image, self).__init__("/image", data)
        self.updateStep("/image", data, self)

    def abs(self):
        operation_type = "abs"
        return self.operation_math(operation_type)

    def add(self, dstiamge):
        operation_type = "add"
        return self.operation(dstiamge, operation_type)

    def addBands(self, srcImg, names: list = None, overwrite: bool = False):
        if srcImg is not None and not isinstance(srcImg, Image):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"srcImg supports only the engine.Image type argument, passed in as {type(srcImg)}"
            )
        if names is not None and not isinstance(names, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"names supports only list type arguments, passed in as {type(names)}"
            )
        if overwrite is not None and not isinstance(overwrite, bool):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"overwrite only the bool parameter is supported. The passed type is {type(overwrite)}",
            )
        data = {
            "dstimage": self,
            "sourceimage": srcImg,
            "names": names,
            "overwrite": overwrite
        }
        funNode = FunctionHelper.apply("/image/addBands", "engine.Image", data)
        return funNode

    def And(self, dstimage):
        logic_type = "and"
        return self.logic(dstimage, logic_type)

    def arccos(self):
        operation_type = "arccos"
        return self.operation_math(operation_type)

    def arcsin(self):
        operation_type = "arcsin"
        return self.operation_math(operation_type)

    def arctan(self):
        operation_type = "arctan"
        return self.operation_math(operation_type)

    def bandNames(self):
        data = {
            "image": self
        }
        return FunctionHelper.apply("/image/bandNames", "engine.Image", data)

    def bitwiseAnd(self, image2, operation_number: int = None):
        bitwise_type = "bitwiseAnd"
        return self.bitwise_AndOrXor(image2, bitwise_type, operation_number)

    def bitwiseNot(self):
        data = {
            "image": self
        }
        return FunctionHelper.apply("/image/bitwiseNot", "engine.Image", data)

    def bitwiseOr(self, image2, operation_number: int = None):
        bitwise_type = "bitwiseOr"
        return self.bitwise_AndOrXor(image2, bitwise_type, operation_number)

    def bitwiseXor(self, image2, operation_number: int = None):
        bitwise_type = "bitwiseXor"
        return self.bitwise_AndOrXor(image2, bitwise_type, operation_number)

    def bitwise_AndOrXor(self, image2, bitwise_type: str, operation_number: int = None):
        if image2 is not None and not isinstance(image2, engine.Image):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"image2 supports only the engine.Image type parameter, passed in as {type(image2)}",
            )
        data = {
            "image1": self,
            "image2": image2,
            "operation_number": operation_number,
            "bitwise_type": bitwise_type
        }
        return FunctionHelper.apply("/image/bitwiseAndOrXor", "engine.Image", data)

    def ceil(self):
        operation_type = "ceil"
        return self.operation_math(operation_type)

    def cast(self, bandTypes: dict):
        if bandTypes is not None and not isinstance(bandTypes, dict):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"bandTypes only supports dict arguments, passed as {type(bandTypes)}",
            )
        data = {
            "image": self,
            "bandTypes": bandTypes
        }

        if "bandTypes" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The bandTypes parameter cannot be empty")

        return FunctionHelper.apply("/image/cast", "engine.Image", data)

    def clip(self, geometry):
        if geometry is not None and not isinstance(geometry, engine.Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry Only supports parameters of the engine.Geometry type, passed in as {type(geometry)}",
            )

        data = {
            "image": self,
            "boundary": {
                "geometry": geometry
            }
        }
        if "boundary" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The boundary parameter cannot be empty")
        fun_node = FunctionHelper.apply("/image/clip", "engine.Image", data)
        return fun_node

    def expression(self, band_index_exp: str, map_dict: dict = None):
        if map_dict is None:
            map_dict = {}
        if band_index_exp is not None and not isinstance(band_index_exp, str):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"names only supports str parameters, passing in {type(band_index_exp)}"
            )
        if map_dict is not None and not isinstance(map_dict, dict):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"names only supports dict arguments, passing in {type(map_dict)}"
            )
        data = {
            "image": self,
            "expression": band_index_exp,
            "map": map_dict
        }
        return FunctionHelper.apply("/image/expression", "engine.Image", data)
    @staticmethod
    def constant(value: Union[int, float, list]):
        data = {}
        if value is not None and not isinstance(value, (int, float, list)):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"Only (int,float,list) arguments are supported for value, passing in {type(value)}",
            )
        if value is not None and isinstance(value, (int, float)):
            data = {
                "constant": [value]
            }
        elif value is not None and isinstance(value, list):
            data = {
                "constant": value
            }
        fun_node = FunctionHelper.apply("/image/constant", "engine.Image", data)
        return fun_node

    def cos(self):
        operation_type = "cos"
        return self.operation_math(operation_type)

    def cosh(self):
        operation_type = "cosh"
        return self.operation_math(operation_type)

    def divide(self, dstimage):
        operation_type = "divide"
        return self.operation(dstimage, operation_type)

    def eq(self, dstimage):
        logic_type = "eq"
        return self.logic(dstimage, logic_type)

    def floor(self):
        operation_type = "floor"
        return self.operation_math(operation_type)

    @staticmethod
    def fromGeometry(geometry, source, options=None):
        if not options:
            options = {"gpu_path": "false"}
        elif not options.get("gpu_path"):
            option = {"gpu_path": "false"}
        data = {
            "geometry": geometry,
            "dataset": source,
            "options": options
        }
        fun_node = FunctionHelper.apply("/image/fromGeometry", "engine.Image", data)
        return fun_node

    def getBound(self):
        data = self
        fun_node = FunctionHelper.apply("/image/getBound", "engine.Image", data)
        return fun_node

    def getCenter(self):
        data = self
        fun_node = FunctionHelper.apply("/image/getCenter", "engine.Image", data)
        return fun_node

    def gt(self, dstimage):
        logic_type = "gt"
        return self.logic(dstimage, logic_type)

    def gte(self, dstimage):
        logic_type = "gte"
        return self.logic(dstimage, logic_type)

    @staticmethod
    def loadLocalImage(path):
        data = {
            "path": path
        }
        fun_node = FunctionHelper.apply("/image/loadLocalImage", "engine.Image", data)
        return fun_node

    def log(self):
        operation_type = "log"
        return self.operation_math(operation_type)

    def log10(self):
        operation_type = "log10"
        return self.operation_math(operation_type)

    def logic(self, dstimage, logic_type: str):
        if dstimage is not None and not isinstance(dstimage, (Image, int)):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"srcImg only supports parameters of type(engine.Image, int), passing {type(dstimage)}"
            )
        if logic_type is not None and not isinstance(logic_type, str):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"srcImg only supports str parameters, passing in {type(logic_type)}"
            )
        data = {
            "image1": self,
            "image2": dstimage,
            "logic_type": logic_type
        }
        fun_node = FunctionHelper.apply("/image/logic", "engine.Image", data)
        return fun_node

    def lt(self, dstimage):
        logic_type = "lt"
        return self.logic(dstimage, logic_type)

    def lte(self, dstimage):
        logic_type = "lte"
        return self.logic(dstimage, logic_type)

    def mask(self):
        data = {
            "image": self
        }
        fun_node = FunctionHelper.apply("/image/mask", "engine.Image", data)
        return fun_node

    def multiply(self, dstimage):
        operation_type = "multiply"
        return self.operation(dstimage, operation_type)

    def ndvi(self, dstimage):
        operation_type = "ndvi"
        return self.operation(dstimage, operation_type)

    def neq(self, dstimage):
        logic_type = "neq"
        return self.logic(dstimage, logic_type)

    def Not(self, dstimage):
        logic_type = "Not"
        return self.logic(dstimage, logic_type)

    def operation(self, dstiamge, operation_type: str):
        if dstiamge is not None and not isinstance(dstiamge, Image):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"srcImg only supports parameters of type engine.Image, which is passed as {type(dstiamge)}"
            )
        if operation_type is not None and not isinstance(operation_type, str):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"bandSelectors only support str parameters, passing in {type(operation_type)}",
            )
        data = {
            "image1": self,
            "image2": dstiamge,
            "operation_type": operation_type
        }
        fun_node = FunctionHelper.apply("/image/image_operation", "engine.Image", data)
        return fun_node

    def operation_math(self, operation_type: str):
        if operation_type is not None and not isinstance(operation_type, str):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"bandSelectors only support str parameters, passing in {type(operation_type)}",
            )
        data = {
            "image": self,
            "operation_type": operation_type
        }
        fun_node = FunctionHelper.apply("/image/image_operation_math", "engine.Image", data)
        return fun_node

    def Or(self, dstimage):
        logic_type = "or"
        return self.logic(dstimage, logic_type)

    def reduce(self, reducer):
        data = {
            "image": self,
            "reducer": reducer
        }
        fun_node = FunctionHelper.apply("/image/reduce", "engine.Image", data)
        return fun_node

    def reduceNeighborhood(self, reducer, kernel: list, scale: [int, float] = 300):
        if kernel is not None and not isinstance(kernel, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"scale only supports list-type parameters, passing in {type(kernel)}"
            )
        if scale is not None and not isinstance(scale, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"scale only supports (int,float) parameters, passing in {type(scale)}"
            )

        data = {
            "image": self,
            "reducer": reducer,
            "kernel": kernel,
            "scale": scale
        }
        fun_node = FunctionHelper.apply("/image/reduceNeighborhood", "engine.Image", data)
        return fun_node

    def reduceRegion(self, reducer, geometry, scale: [int, float] = 300):
        if geometry is not None and not isinstance(geometry, engine.Geometry):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"geometry Only supports parameters of the engine.Geometry type, passed in as {type(geometry)}",
            )
        if scale is not None and not isinstance(scale, (int, float)):
            raise RSError(
                RSErrorCode.ARGS_ERROR, f"scale only supports arguments of type(int,float), passed in as {type(scale)}"
            )

        data = {
            "image": self,
            "reducer": reducer,
            "geometry": geometry,
            "scale": scale
        }
        if "reducer" not in data:
            raise RSError(RSErrorCode.ARGS_ERROR, "The reducer parameter cannot be empty")
        fun_node = FunctionHelper.apply("/image/reduceRegion", "engine.Image", data)
        return fun_node

    def rename(self, var_args: list):
        if var_args is not None and not isinstance(var_args, list):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"bandSelectors only support list arguments, passing in {type(var_args)}",
            )
        data = {
            "image": self,
            "var_args": var_args
        }
        fun_node = FunctionHelper.apply("/image/rename", "engine.Image", data)
        return fun_node

    def select(self, bandSelectors: Union[str, list]):
        if bandSelectors is not None and not isinstance(bandSelectors, (str, list)):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"bandSelectors accepts only (str,list) arguments, passing in {type(bandSelectors)}",
            )
        data = {
            "image": self,
            "bands": bandSelectors
        }
        fun_node = FunctionHelper.apply("/image/select", "engine.Image", data)
        return fun_node

    def sin(self):
        operation_type = "sin"
        return self.operation_math(operation_type)

    def sinh(self):
        operation_type = "sinh"
        return self.operation_math(operation_type)

    def subtract(self, dstimage):
        operation_type = "subtract"
        return self.operation(dstimage, operation_type)

    def tan(self):
        operation_type = "tan"
        return self.operation_math(operation_type)

    def tanh(self):
        operation_type = "tanh"
        return self.operation_math(operation_type)

    def where(self, conditionimage, value: int):
        if conditionimage is not None and not isinstance(conditionimage, Image):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"srcImg only supports parameters of type engine.Image, which is passed in as {type(conditionimage)}"
            )
        if value is not None and not isinstance(value, int):
            raise RSError(
                RSErrorCode.ARGS_ERROR,
                f"srcImg only supports int parameters, passing in {type(value)}"
            )
        data = {
            "sourceimage": self,
            "conditionimage": conditionimage,
            "value": value
        }
        fun_node = FunctionHelper.apply("/image/where", "engine.Image", data)
        return fun_node
