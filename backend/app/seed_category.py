from app.core.database import SessionLocal
from app.models.category import Category

db = SessionLocal()
categories = ["Listening", "Structure", "Reading"]
for name in categories:
    if not db.query(Category).filter_by(name=name).first():
        db.add(Category(name=name))
db.commit()
db.close()
print("Seed data selesai!")