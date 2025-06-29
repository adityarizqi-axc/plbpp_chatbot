from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
        
        