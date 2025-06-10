from pydantic import BaseModel

class FAQBase(BaseModel):
    question: str
    answer: str
    category_id: int

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: str = None
    answer: str = None
    category_id: int = None

class FAQOut(FAQBase):
    id: int

    class Config:
        orm_mode = True