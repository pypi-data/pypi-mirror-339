# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class RSErrorCode(object):
    DEFAULT_INTERNAL_ERROR = 100000

    # ENVIRONMENT_INIT_ERROR = 22306001
    # JOB_CANCELLED = 22306003
    ARGS_ERROR = 200000


class RSError(Exception):
    DEFAULT_ERROR_MESSAGE = "ERROR_UNKNOWN"

    def __init__(self, code: int = RSErrorCode.DEFAULT_INTERNAL_ERROR, message: str = "",
                 troubleshooting_information: str = ""):
        debug_info = ""
        if troubleshooting_information != json.dumps({}):
            debug_info = troubleshooting_information
        if str(code).startswith("1") or str(code).startswith("2"):
            super().__init__("[RSError]: {}, {}. {}".format(
                code, message, debug_info))
        else:
            super().__init__("{}. {}".format(
                RSError.DEFAULT_ERROR_MESSAGE, debug_info))

