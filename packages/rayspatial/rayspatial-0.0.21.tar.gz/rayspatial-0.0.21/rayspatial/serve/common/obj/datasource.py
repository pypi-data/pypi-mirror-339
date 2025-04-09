from pydantic import BaseModel
from typing import (
    Any,
    Union,
    List
)


class StacDataConstructor(BaseModel):
    max_items: Union[int, None] = None
    limit: Union[int, None] = None
    ids: Union[List[str],str, None] = None
    collections: Union[List[str],str, None] = None
    bbox: Union[List[float], None] = None
    intersects: Union[dict[str, Any], None] = None
    datetime: Union[List[str],str, None] = None
    query: Union[str, None] = None
    filter: Union[dict, None] = None
    filter_lang: Union[dict, None] = None
    sortby: Union[dict, None] = None
    fields: Union[dict, None] = None