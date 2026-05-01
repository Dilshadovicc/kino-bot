import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. SOZLAMALAR
TOKEN = "8321676949:AAGNY5jPNiN1TA293TrI7W3-JnxltZ4Y34M"
ADMIN_ID = 6288457586  # Sizning ID raqamingiz
DB_FILE = "movies_db.json"

# 2. BAZA BILAN ISHLASH
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

movies = load_db()

# 3. BUYRUQLAR
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Salom! Kino kodini yozing:")

# Kino qo'shish (Faqat Admin uchun)
async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return 

    if update.message.caption and "KOD:" in update.message.caption.upper():
        parts = update.message.caption.upper().split("KOD:")
        code = parts[1].strip()
        file_id = update.message.video.file_id
        
        movies[code] = file_id
        save_db(movies)
        await update.message.reply_text(f"✅ Saqlandi! Kod: {code}")
    else:
        await update.message.reply_text("⚠️ Videoni yuboring va tagiga 'KOD: A1' deb yozing!")

# Kinoni o'chirish (Faqat Admin uchun)
async def delete_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ O'chirish uchun kodni ham yozing. Masalan: /del A1")
        return

    code = context.args[0].upper()
    if code in movies:
        del movies[code]
        save_db(movies)
        await update.message.reply_text(f"🗑 Kod {code} bazadan o'chirildi!")
    else:
        await update.message.reply_text(f"❓ Kod {code} topilmadi.")

# Kino yuborish (Hamma uchun)
async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.upper()
    if text in movies:
        await update.message.reply_video(video=movies[text], caption=f"Kino kodi: {text}")
    else:
        await update.message.reply_text("❌ Kechirasiz, bunday kodli kino topilmadi.")

# 4. BOTNI ISHGA TUSHIRISH
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("del", delete_movie)) # O'chirish buyrug'i
    app.add_handler(MessageHandler(filters.VIDEO, add_movie))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie))
    
    print("Bot yangilandi va ishga tushdi...")
    app.run_polling()