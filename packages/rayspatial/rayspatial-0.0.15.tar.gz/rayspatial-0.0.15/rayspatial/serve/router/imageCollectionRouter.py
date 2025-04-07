from rayspatial.serve.common.obj.requestHeader import RsHeader
from rayspatial.serve.common.route import Routers
from rayspatial.serve.core.actor.coreActor import general_execute_method
from rayspatial.serve.common.obj.imageCollection import FromImagesImageModel, MosaicImageModel, LoadLocalImageCollectionModel, SelectImageCollectionModel
imageCollectionRoutes = Routers()
imageCollectionBaseRoutes = "/imageCollection"

@imageCollectionRoutes.route(f"{imageCollectionBaseRoutes}/fromImages")
def fromImages(header: RsHeader, inputParams: FromImagesImageModel):
    res = general_execute_method(header, f"{imageCollectionBaseRoutes}/fromImages", inputParams)
    return res


@imageCollectionRoutes.route(f"{imageCollectionBaseRoutes}/loadLocalImageCollection")
def loadLocalImageCollection(header: RsHeader, inputParams: LoadLocalImageCollectionModel):
    res = general_execute_method(header, f"{imageCollectionBaseRoutes}/loadLocalImageCollection", inputParams)
    return res

@imageCollectionRoutes.route(f"{imageCollectionBaseRoutes}/mosaic")
def mosaic(header: RsHeader, inputParams: MosaicImageModel):
    res = general_execute_method(header, f"{imageCollectionBaseRoutes}/mosaic", inputParams)
    return res

@imageCollectionRoutes.route(f"{imageCollectionBaseRoutes}/select")
def select(header: RsHeader, inputParams: SelectImageCollectionModel):
    res = general_execute_method(header, f"{imageCollectionBaseRoutes}/select", inputParams)
    return res