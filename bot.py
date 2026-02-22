import os
import logging
import asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

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

# Flask app
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "✅ Bot is running!"

@app_flask.route('/health')
def health():
    return "OK", 200

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

async def run_bot_async():
    """تشغيل البوت بشكل غير متزامن"""
    # إنشاء التطبيق
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    logger.info("✅ البوت بدأ العمل...")
    
    # بدء البوت
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # إبقاء البوت شغالاً
    try:
        while True:
            await asyncio.sleep(3600)  # انتظر ساعة ثم تحقق
    except asyncio.CancelledError:
        pass
    finally:
        # إيقاف التشغيل
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

def run_flask():
    """تشغيل Flask"""
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # تشغيل Flask في عملية منفصلة (أسهل وأضمن)
    import multiprocessing
    
    # تشغيل Flask في عملية منفصلة
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()
    
    # تشغيل البوت في العملية الرئيسية
    try:
        asyncio.run(run_bot_async())
    except KeyboardInterrupt:
        logger.info("🛑 إيقاف البوت...")
        flask_process.terminate()
        flask_process.join()
