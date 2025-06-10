from sqlalchemy.orm import Session
from ..models.faq import FAQ
from ..schemas.faq_schema import FAQCreate, FAQUpdate

def get_faqs(db: Session, category_id: int = None):
    if category_id:
        return db.query(FAQ).filter(FAQ.category_id == category_id).all()
    return db.query(FAQ).all()

def get_faq(db: Session, faq_id: int):
    return db.query(FAQ).filter(FAQ.id == faq_id).first()

def create_faq(db: Session, faq: FAQCreate):
    db_faq = FAQ(**faq.dict())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq

def update_faq(db: Session, faq_id: int, faq: FAQUpdate):
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not db_faq:
        return None
    for attr, value in faq.dict(exclude_unset=True).items():
        setattr(db_faq, attr, value)
    db.commit()
    db.refresh(db_faq)
    return db_faq

def delete_faq(db: Session, faq_id: int):
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not db_faq:
        return None
    db.delete(db_faq)
    db.commit()
    return db_faq