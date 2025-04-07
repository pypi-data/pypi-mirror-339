from rayspatial.serve.common.route import Routers
from rayspatial.serve.common.obj.requestHeader import RsHeader
from rayspatial.serve.common.obj.datasource import StacDataConstructor
from rayspatial.serve.core.actor.coreActor import general_execute_method

datasourceRoutes = Routers()
datasourceBaseRoutes = "/datasource"

@datasourceRoutes.route(f"{datasourceBaseRoutes}/stac/imageCollection")
def stac_imageCollection(header: RsHeader, inputParams: StacDataConstructor):
    res = general_execute_method(header, f"{datasourceBaseRoutes}/stac/imageCollection", inputParams)
    return res

@datasourceRoutes.route(f"{datasourceBaseRoutes}/stac/image")
def stac_image(header: RsHeader, inputParams: StacDataConstructor):
    res = general_execute_method(header, f"{datasourceBaseRoutes}/stac/image", inputParams)
    return res
