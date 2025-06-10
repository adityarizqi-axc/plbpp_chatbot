import logging
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler,
)
import requests
import os

# Set your bot token here or via environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN", "7853926867:AAGW0_8fQtWV_IkNPTzdiY1dO-Oaq5iJGZ0")
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATE_CATEGORY, STATE_QUESTION = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get categories from backend
    resp = requests.get(f"{API_URL}/categories/")
    categories = resp.json()
    print("DEBUG categories:", categories)
    print("DEBUG type:", type(categories))
    if len(categories) > 0:
        print("DEBUG type first item:", type(categories[0]))
    try:
        buttons = [[KeyboardButton(cat['name'])] for cat in categories]
    except Exception as e:
        print("ERROR membuat tombol kategori:", e)
        print("ISI categories:", categories)
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Selamat datang di Chatbot TOEFL! Silakan pilih kategori pertanyaan:",
        reply_markup=reply_markup
    )
    context.user_data['categories'] = {cat['name']: cat['id'] for cat in categories}
    return STATE_CATEGORY

async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_name = update.message.text
    cat_id = context.user_data['categories'].get(cat_name)
    if not cat_id:
        await update.message.reply_text("Kategori tidak dikenali, silakan pilih dari daftar.")
        return STATE_CATEGORY
    # Get FAQ list for category
    resp = requests.get(f"{API_URL}/faqs/?category_id={cat_id}")
    faqs = resp.json()
    if not faqs:
        await update.message.reply_text("Belum ada pertanyaan di kategori ini.")
        return STATE_CATEGORY
    context.user_data['faqs'] = {faq['question']: faq for faq in faqs}
    buttons = [[KeyboardButton(faq['question'])] for faq in faqs]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Silakan pilih pertanyaan:", reply_markup=reply_markup)
    return STATE_QUESTION

async def choose_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text
    faq = context.user_data['faqs'].get(q)
    if faq:
        await update.message.reply_text(f"Jawaban:\n{faq['answer']}")
        return ConversationHandler.END
    # If not found, try AI
    await update.message.reply_text("Mencoba mencari jawaban dari AI...")
    ai_resp = requests.post(f"{API_URL}/ask-ai", json={"question": q})
    if ai_resp.status_code == 200 and ai_resp.json().get("answer"):
        await update.message.reply_text(f"AI Menjawab:\n{ai_resp.json()['answer']}")
    else:
        await update.message.reply_text("Maaf, pertanyaan tidak ditemukan. Silakan buat tiket di link berikut: [Tiket Support](https://link-tiket.com)", disable_web_page_preview=True)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Terima kasih telah menggunakan Chatbot TOEFL.")
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_category)],
            STATE_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_question)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()