
from rayspatial.serve.core.dataframe.imageDataFrame import ImageDataFrame
from rayspatial.serve.common.obj.image import Image
from rayspatial.serve.common.obj.imageCollection import ImageCollection
from rayspatial.serve.core.utils.imageUtils import ImageUtils


def format_result_image(image:Image):
    image = ImageDataFrame.ignore_image_dataframe_to_image(image)
    image = ImageUtils.sort_image_bands(image)
    return image

def handle_result(result):
    if isinstance(result, Image):
        result = format_result_image(result)
    elif isinstance(result, ImageCollection):
        for image in result.images:
            image = format_result_image(image)
    return result
