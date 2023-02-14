from pydantic import BaseModel
from typing import Union, List


class ItemBase(BaseModel):
    title = str
    description = str
    done = bool
    priority = int

class ItemCreate(ItemBase):
    title = str
    description = str
    done = bool
    priority = int


class Item(ItemBase):
    id = int

    class Config:
        orm_mode = True
        extra = "forbid"


class ItemUpdate(ItemBase):
    pass


class ItemPatch(ItemBase):
    pass

# class RequestPayloadService(BaseModel):
#     """
#     Request payload service
#     """

#     header: RequestPayloadHeader = Field(...)
#     params: Union[RequestPayloadPositionsParams, RequestPayloadOrdersParams] = Field(
#         ...
#     )