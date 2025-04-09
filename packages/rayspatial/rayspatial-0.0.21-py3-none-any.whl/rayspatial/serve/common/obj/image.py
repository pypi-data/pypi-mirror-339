import os
from datetime import datetime
from typing import Union, Any, List

from pydantic import BaseModel


class Band(BaseModel):
    id: Union[str, None] = None
    type: Union[str, None] = "Band"
    crs: Union[str, int, None] = None
    crs_transform: Union[list, None] = None
    data_type: Union[str, None] = None
    max: Union[int, float, str, None] = None
    min: Union[int, float, str, None] = None
    precision: Union[str, None] = None
    tif_url: Union[str, None] = None
    properties: Union[dict, None] = None
    nodata: Union[Any, None] = None
    geometry: Union[str, None] = None
    image_id: Union[str, None] = None
    width: Union[int, None] = None
    height: Union[int, None] = None
    size: Union[int, None] = None
    bbox: Union[list, None] = None
    center: Union[list, None] = None
    band_data: Union[list, None] = None


class Image(BaseModel):
    id: Union[str, None] = None
    type: Union[str, None] = "Image"
    bands: Union[list[Band], None] = None
    bands_data: Union[Any, None] = None
    properties: Union[dict, None] = None
    url: Union[str, None] = None
    flag_id: Union[str, None] = datetime.now().strftime(f"%Y_%m{os.sep}%d{os.sep}%H%M%S%f")


class ImageConstructor(BaseModel):
    id: Union[str, None] = None


class LoadLocalImageModel(BaseModel):
    path: Union[str]
    

class ImageOperationModel(BaseModel):
    image1: Union[Image, None] = None
    image2: Union[Image, int, float, None] = None


class ImageSelectModel(BaseModel):
    image: Union[Image, None] = None
    var_args: Union[str,int,list,list[list],None] = None
    
