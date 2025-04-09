from typing import Union, Any
from datetime import datetime
from pydantic import BaseModel, Field

from .image import Image


class ImageCollection(BaseModel):
    id: Union[str, None] = Field(f"id_{datetime.now().strftime('%Y%m%d%H%M%S%f')}", description="image collection id")
    version: Union[str, int, None] = Field(None, description="image collection version")
    type: Union[str, None] = Field('ImageCollection', description="image collection type")
    properties: Any = Field({}, description="image collection properties")
    images: Union[list[Image], None] = Field([], description="image collection")
    searchFlag: Union[bool, None] = Field(False)
    searchSql: Union[str, None] = Field(None)
    searchParam: Union[dict, None] = Field(None)
    selectors: Union[list, str, None] = Field(None)
    names: Union[list, None] = Field(None)
    selectorsNamsFlag: Union[bool, None] = Field(False)

class FromImagesImageModel(BaseModel):
    images: Union[list[Image], None] = Field(None)
    

class LoadLocalImageCollectionModel(BaseModel):
    path: Union[str, None] = Field(None)
    limit_images: Union[int, None] = Field(None, description="limit images")

class MosaicImageModel(BaseModel):
    imageCollection: Union[ImageCollection, None] = Field(None)
    method: Union[str, None] = Field('first', examples=["first","last","mean","median","count","sum","max","min","std"],description="mosaic type")
    


class SelectImageCollectionModel(BaseModel):
    imageCollection: Union[ImageCollection, None] = Field(None)
    selectors: Union[str, list, int, None] = Field(None)
    names: Union[list, None] = Field(None)