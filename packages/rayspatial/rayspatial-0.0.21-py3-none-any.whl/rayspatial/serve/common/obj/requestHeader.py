from typing import Union
from pydantic import Field
from pydantic import BaseModel
import uuid

class RsHeader(BaseModel):
    scale: Union[float, None] = None
    bbox: Union[list, None] = None
    route: Union[str, None] = Field(default="map", example="map,value")
    timestamp: Union[str, None] = None
    method: Union[str, None] = None
    resultBbox: Union[str, None] = None
    startTime: Union[str, None] = None
    resultLibType: Union[str, None] = None
    requestDay: Union[str, None] = None
    id:Union[str,None] = None
    
