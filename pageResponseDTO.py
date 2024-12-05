from pydantic import BaseModel
from typing import List

class page_response_dto(BaseModel):
    dtoList: List[dict]
    pageNumList: List[int]
    prev: bool
    next: bool
    totalCount: int
    totalPage: int
    current: int
    prevPage: int = None
    nextPage: int = None
