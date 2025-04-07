from rayspatial.serve.common.obj.image import ImageConstructor, ImageOperationModel, LoadLocalImageModel, ImageSelectModel
from rayspatial.serve.common.obj.requestHeader import RsHeader
from rayspatial.serve.common.route import Routers
from rayspatial.serve.core.actor.coreActor import general_execute_method

imageRoutes = Routers()
imageBaseRoutes = "/image"


@imageRoutes.route(f"{imageBaseRoutes}")
def image(header: RsHeader, inputParams: ImageConstructor):
    res = general_execute_method(header, f"{imageBaseRoutes}", inputParams)
    return res


@imageRoutes.route(f"{imageBaseRoutes}/loadLocalImage")
def loadLocalImage(header: RsHeader, inputParams: LoadLocalImageModel):
    res = general_execute_method(header, f"{imageBaseRoutes}/loadLocalImage", inputParams)
    return res


@imageRoutes.route(f"{imageBaseRoutes}/add")
def add(header: RsHeader, inputParams: ImageOperationModel):
    res = general_execute_method(header, f"{imageBaseRoutes}/add", inputParams)
    return res


@imageRoutes.route(f"{imageBaseRoutes}/subtract")
def delete(header: RsHeader, inputParams: ImageOperationModel):
    res = general_execute_method(header, f"{imageBaseRoutes}/subtract", inputParams)
    return res


@imageRoutes.route(f"{imageBaseRoutes}/multiply")
def multiply(header: RsHeader, inputParams: ImageOperationModel):
    res = general_execute_method(header, f"{imageBaseRoutes}/multiply", inputParams)
    return res


@imageRoutes.route(f"{imageBaseRoutes}/divide")
def divide(header: RsHeader, inputParams: ImageOperationModel):
    res = general_execute_method(header, f"{imageBaseRoutes}/divide", inputParams)
    return res

@imageRoutes.route(f"{imageBaseRoutes}/select")
def select(header: RsHeader, inputParams: ImageSelectModel):
    res = general_execute_method(header, f"{imageBaseRoutes}/select", inputParams)
    return res


