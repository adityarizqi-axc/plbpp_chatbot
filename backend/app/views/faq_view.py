from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..schemas.faq_schema import FAQOut, FAQCreate, FAQUpdate
from ..controllers.faq_controller import (
    get_faqs, get_faq, create_faq, update_faq, delete_faq
)
from ..core.database import get_db
from ..services.auth_service import get_current_admin

router = APIRouter(prefix="/faqs", tags=["faqs"])

@router.get("/", response_model=list[FAQOut])
def api_get_faqs(category_id: int = Query(None), db: Session = Depends(get_db)):
    return get_faqs(db, category_id)

@router.get("/{faq_id}", response_model=FAQOut)
def api_get_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = get_faq(db, faq_id)
    if not faq:
        raise HTTPException(404, "FAQ not found")
    return faq

@router.post("/", response_model=FAQOut)
def api_create_faq(faq: FAQCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return create_faq(db, faq)

@router.put("/{faq_id}", response_model=FAQOut)
def api_update_faq(faq_id: int, faq: FAQUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    updated = update_faq(db, faq_id, faq)
    if not updated:
        raise HTTPException(404, "FAQ not found")
    return updated

@router.delete("/{faq_id}", response_model=FAQOut)
def api_delete_faq(faq_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    deleted = delete_faq(db, faq_id)
    if not deleted:
        raise HTTPException(404, "FAQ not found")
    return deleted