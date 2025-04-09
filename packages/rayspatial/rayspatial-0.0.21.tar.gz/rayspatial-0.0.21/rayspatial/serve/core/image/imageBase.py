import os

from rayspatial.serve.common.obj.image import LoadLocalImageModel, ImageOperationModel, ImageSelectModel
from rayspatial.serve.core.image.imageOperate import ImageOperate
from rayspatial.serve.core.utils.fileUtils import FileUtils
from rayspatial.serve.core.utils.imageUtils import ImageUtils


class ImageBase:

    def _image(self, header, params):
        return f"{params}+ImageBase+111"

    def _image_add(self, header, params: ImageOperationModel):
        return ImageOperate.two_image_math_operate(header, params.image1, params.image2, "+")
    
    def _image_subtract(self, header, params: ImageOperationModel):
        return ImageOperate.two_image_math_operate(header, params.image1, params.image2, "-")
    
    def _image_multiply(self, header, params: ImageOperationModel):
        return ImageOperate.two_image_math_operate(header, params.image1, params.image2, "*")
    
    def _image_divide(self, header, params: ImageOperationModel):
        return ImageOperate.two_image_math_operate(header, params.image1, params.image2, "/")

    def _image_loadLocalImage(self, header, params: LoadLocalImageModel):
        assert os.path.exists(params.path), f"path {params.path} not exist"
        image_paths = FileUtils.get_all_image_files(params.path)
        image = ImageUtils.cover_paths_to_image_obj(image_paths)
        return image

    def _image_select(self, header, params: ImageSelectModel):
        return ImageOperate.select_image_band(header, params.image, params.var_args)

