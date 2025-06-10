from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.admin_schema import AdminLogin, AdminOut
from ..controllers.admin_controller import authenticate_admin, create_admin
from ..core.security import create_access_token
from ..core.database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/login")
def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token({"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Only for initial admin creation during setup (disable after use in prod!)
@router.post("/register", response_model=AdminOut)
def register_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    return create_admin(db, admin.username, admin.password)