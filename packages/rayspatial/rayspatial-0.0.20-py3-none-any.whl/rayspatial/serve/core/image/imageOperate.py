import re
from rayspatial.serve.common.obj.image import Image
from rayspatial.serve.core.dataframe.imageDataFrame import ImageDataFrame


class ImageOperate:
    @staticmethod
    def two_image_math_operate(header, image1, image2, operateType):
        image_1 = ImageDataFrame.format_image_bands_data(image1, header)
        if isinstance(image2, Image):
            image2 = ImageDataFrame.format_image_bands_data(image2, header)
        return ImageDataFrame.two_image_operate(image_1, image2, operateType)

    @staticmethod
    def select_image_band(header, image, var_args):
        bandNames = var_args
        newNames = None
        if type(var_args) == str:
            bandNames = var_args.split(",")
        elif type(var_args) == int:
            bandNames = [image.bands[var_args].id]
        elif type(var_args) == list:
            bandNames = var_args
        elif type(var_args) == list[list]:
            bandNames = var_args[0]
            newNames = var_args[1]
        filterBands = []
        for bandName in bandNames:
            if isinstance(bandName, int):
                filterBands.append(image.bands[bandName])
            else:
                for band in image.bands:
                    if band.id == bandName or re.fullmatch(bandName, band.id):
                        filterBands.append(band)
        image.bands = filterBands

        if newNames:
            for band in image.bands:
                if band.id in newNames:
                    band.id = newNames[band.id]

        return image
