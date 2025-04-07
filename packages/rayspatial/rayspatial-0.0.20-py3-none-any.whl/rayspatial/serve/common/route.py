import inspect


class Route:
    def __init__(self, path, func, param_info):
        self.path = path
        self.func = func
        self.param_info = param_info


class Routers:
    routes_map = None

    def __init__(self, routes_map=None):
        if not routes_map:
            self.routes_map = {}
        else:
            self.routes_map = dict(routes_map)

    def route(self, path):
        def decorator(func):
            signature = inspect.signature(func)
            params = signature.parameters
            param_info = {}
            for index, (param_name, param) in enumerate(params.items()):
                param_info.update({param_name: param.annotation})
            self.routes_map.update({path: Route(path, func, param_info)})
            return func

        return decorator
