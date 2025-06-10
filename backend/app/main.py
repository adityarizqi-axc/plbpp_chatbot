from fastapi import FastAPI
from .core.database import Base, engine
from .views import category_router, faq_router, admin_router
from .views.ai_view import router as ai_router
from app.views.category_view import router as category_router
from app.views.ai_view import router as ai_router
import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
# Create tables
Base.metadata.create_all(bind=engine)
API_URL = "http://localhost:8000/api/v1"

app = FastAPI(
    title="TOEFL Chatbot Backend",
    description="API backend untuk chatbot TOEFL dan admin web"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resp = requests.get(f"{API_URL}/categories/")
        resp.raise_for_status()
        categories = resp.json()
    except Exception:
        await update.message.reply_text("Gagal mengambil kategori dari server.")
        return

    # Hanya buat tombol jika data sesuai, tidak kirim isi categories ke user
    if isinstance(categories, list) and categories and isinstance(categories[0], dict) and 'name' in categories[0]:
        buttons = [[KeyboardButton(cat['name'])] for cat in categories]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(
            "Pilih kategori soal TOEFL:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("Format data kategori tidak sesuai. Silakan hubungi admin.")


# Register routers
app.include_router(admin_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(faq_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
