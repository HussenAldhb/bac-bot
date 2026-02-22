import os
import logging
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask app
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "✅ Bot is running!"

# المتغيرات
TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود")
if not WEB_APP_URL:
    raise ValueError("❌ WEB_APP_URL غير موجود")

# إعداد التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start"""
    keyboard = [
        [InlineKeyboardButton("🚀 فتح المنصة التعليمية", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "مرحباً بك في بوت بكالوريا+! 👋\n"
        "اضغط على الزر لفتح المنصة:",
        reply_markup=reply_markup
    )

def run_bot():
    """تشغيل البوت"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    logger.info("✅ البوت بدأ العمل...")
    # استخدام polling عادي بدون run_polling (لتجنب مشكلة الخيوط)
    app.run_polling(allowed_updates=['message'])

if __name__ == "__main__":
    # تشغيل البوت أولاً
    import threading
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # تشغيل Flask
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
