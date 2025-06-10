from sqlalchemy.orm import Session
from app.models.admin import Admin
from app.core.security import verify_password, create_password_hash

def authenticate_admin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin and verify_password(password, admin.password_hash):
        return admin
    return None

def create_admin(db: Session, username: str, password: str):
    password_hash = create_password_hash(password)
    admin = Admin(username=username, password_hash=password_hash)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin