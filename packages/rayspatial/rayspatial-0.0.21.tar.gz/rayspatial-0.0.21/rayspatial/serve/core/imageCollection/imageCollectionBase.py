import os
from rayspatial.serve.common.obj.image import Image
from rayspatial.serve.common.obj.imageCollection import FromImagesImageModel, MosaicImageModel, LoadLocalImageCollectionModel, SelectImageCollectionModel
from rayspatial.serve.common.obj.imageCollection import ImageCollection
from rayspatial.serve.core.imageCollection.imageCollectionOptions import ImageCollectionOptions
from rayspatial.serve.core.utils.fileUtils import FileUtils
from rayspatial.serve.core.utils.imageUtils import ImageUtils
import re

class ImageCollectionBase:
    
    def __init__(self):
        pass

    def _imageCollection_fromImages(self, header, params: FromImagesImageModel):
        imageCollection = ImageCollection()
        imageCollection.images = params.images
        return imageCollection

    def _imageCollection_mosaic(self, header, params: MosaicImageModel):
        if len(params.imageCollection.images) == 0:
            raise ValueError("images is empty")
        if len(params.imageCollection.images) == 1:
            return params.imageCollection.images[0]
        else:
            return ImageCollectionOptions.mosaic(header, params.imageCollection.images,params.method)
        
    def _imageCollection_loadLocalImageCollection(self, header, params: LoadLocalImageCollectionModel):
        imageCollection = ImageCollection()
        for index, imagePath in enumerate(os.listdir(params.path)):
            if params.limit_images and index >= params.limit_images:
                break
            image_paths = FileUtils.get_all_image_files(os.path.join(params.path, imagePath))
            image = ImageUtils.cover_paths_to_image_obj(image_paths)
            imageCollection.images.append(image)
        return imageCollection

    def _imageCollection_select(self, header, params: SelectImageCollectionModel):
        if params.selectors is None:
            return params.imageCollection
        if isinstance(params.selectors, str):
            for image in params.imageCollection.images:
                tmp_bands = []
                for band in image.bands:
                    if band.id == params.selectors or re.match(params.selectors, band.id):
                        tmp_bands.append(band)
                image.bands = tmp_bands
        elif isinstance(params.selectors, list):
            for image in params.imageCollection.images:
                tmp_bands = []
                for band in image.bands:
                    for select in params.selectors:
                        if isinstance(select, str):
                            if band.id == select or re.match(select, band.id):
                                tmp_bands.append(band)
                        elif isinstance(select, int):
                            tmp_bands.append(image.bands[select])
                image.bands = tmp_bands
        elif isinstance(params.selectors, int):
            for image in params.imageCollection.images:
                if params.selectors > len(image.bands):
                    image.bands = []
                else:
                    image.bands = [image.bands[params.selectors]]
        return params.imageCollection