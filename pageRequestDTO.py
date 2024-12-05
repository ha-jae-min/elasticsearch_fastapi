from pydantic import BaseModel, Field

class page_request_dto(BaseModel):
    page: int = Field(1, ge=1, description="페이지 번호")
    size: int = Field(10, le=100, description="페이지 크기")
    keyword: str = None
    type: str = None
    inventoryID: int = None
    categoryID: int = None
    sort: str = None
