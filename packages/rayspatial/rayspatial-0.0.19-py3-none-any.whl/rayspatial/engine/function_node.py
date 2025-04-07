# !/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
from rayspatial.engine.client.interactive_session import InteractiveSession


class Rs(object):
    stepNum = 0
    step = []
    params = {}

    node_chain_dict = dict()

    def updateStep(self, key, args, step_result_obj_ref):
        step_num = self.incr_step_num()
        rayspatial.step.append({"key": key, "args": args, "stepNum": step_num})
        rayspatial.params[step_result_obj_ref] = step_num

    def incr_step_num(self):
        step = f"${rayspatial.stepNum}"
        rayspatial.stepNum += 1
        return step

    def job(self, scale=0.5):
        from rayspatial.engine.function_helper import FunctionHelper
        data = {"result": self, "scale": scale}
        fun_node = FunctionHelper.apply("Image.BatchProcessing", "engine.Image", data)
        self.updateStep("/image/BatchProcessing", data, fun_node)
        return fun_node


class FunctionNode(object):
    stepNum = 0

    def __init__(self, name, data):
        self.func_name = name
        self.data = data
        self.step = []
        self.params = {}

    def updateStep(self, key, args, step_result_obj_ref):
        step_num = self.incr_step_num()
        self.step.append({"key": key, "args": args, "stepNum": step_num})
        self.params[step_result_obj_ref] = step_num
        return self

    def incr_step_num(self):
        step = f"${FunctionNode.stepNum}"
        FunctionNode.stepNum += 1
        return step

    def job(self, scale=0.5):
        from rayspatial.engine.function_helper import FunctionHelper
        data = {"result": self, "scale": scale}
        fun_node = FunctionHelper.apply("/image/BatchProcessing", "engine.Image", data)
        print(222, fun_node.__dict__)
        return fun_node

    def getInfo(self):
        return InteractiveSession.getInfo(self)
    #
    # def getBound(self):
    #     return InteractiveSession.getBounds(self)

