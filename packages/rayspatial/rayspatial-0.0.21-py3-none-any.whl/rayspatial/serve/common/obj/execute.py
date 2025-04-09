from typing import Union, Any, List

from pydantic import BaseModel


class OperatorModel(BaseModel):
    order: Union[str, None] = None
    router: Union[str, None] = None
    params: Union[Any, None] = None
    resultLibType: Union[str, None] = None


class ExecuteOperationModel(BaseModel):
    id: Union[str, None] = None
    zxy: Union[str, None] = None
    executeObjectKey: Union[str, None] = None
    executeObject: Union[Any, None] = None
    operatorArr: Union[List[OperatorModel], None] = None
    asyncFlag: Union[bool, None] = False
