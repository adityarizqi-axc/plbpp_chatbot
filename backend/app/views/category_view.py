from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.category_schema import CategoryOut, CategoryCreate, CategoryUpdate
from ..controllers.category_controller import (
    get_categories, get_category, create_category, update_category, delete_category
)
from ..core.database import get_db
from ..services.auth_service import get_current_admin
from app.models.category import Category
from app.core.database import get_db
from typing import List

router = APIRouter()

@router.get("/categories/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories  # Harus list of dict dengan key 'name'

@router.get("/", response_model=list[CategoryOut])
def api_get_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@router.get("/{category_id}", response_model=CategoryOut)
def api_get_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category

@router.post("/", response_model=CategoryOut)
def api_create_category(category: CategoryCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return create_category(db, category)

@router.put("/{category_id}", response_model=CategoryOut)
def api_update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    updated = update_category(db, category_id, category)
    if not updated:
        raise HTTPException(404, "Category not found")
    return updated

@router.delete("/{category_id}", response_model=CategoryOut)
def api_delete_category(category_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    deleted = delete_category(db, category_id)
    if not deleted:
        raise HTTPException(404, "Category not found")
    return deleted