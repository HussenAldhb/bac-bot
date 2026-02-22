"""
بوت تيليغرام لفتح منصة بكالوريا+
يعمل مع Render + Flask لضمان الاستضافة
"""

import os          # للوصول إلى متغيرات البيئة
import logging     # لتسجيل الأحداث
import threading   # لتشغيل Flask والبوت معًا
from flask import Flask  # خادم ويب بسيط لإبقاء Render سعيدًا
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------- إعداد Flask ----------
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    """صفحة بسيطة للتأكد من أن الخدمة تعمل"""
    return "✅ Bot is running!"

# ---------- إعداد البوت ----------
# قراءة التوكن ورابط الموقع من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

# التحقق من وجود المتغيرات (في حال النسيان)
if not TOKEN:
    raise ValueError("❌ لم يتم تعيين BOT_TOKEN في متغيرات البيئة")
if not WEB_APP_URL:
    raise ValueError("❌ لم يتم تعيين WEB_APP_URL في متغيرات البيئة")

# إعداد نظام التسجيل (log)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    دالة تنفذ عند إرسال الأمر /start.
    ترسل رسالة تحتوي على زر يفتح تطبيق الويب.
    """
    # إنشاء زر من نوع Web App
    keyboard = [
        [InlineKeyboardButton("🚀 فتح المنصة التعليمية", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة مع الزر
    await update.message.reply_text(
        "مرحباً بك في بوت بكالوريا+! 👋\n"
        "اضغط على الزر لفتح المنصة مباشرة داخل تيليغرام:",
        reply_markup=reply_markup
    )

def run_bot():
    """
    تشغيل البوت في خيط منفصل (polling).
    """
    # إنشاء التطبيق
    app = Application.builder().token(TOKEN).build()
    
    # إضافة معالج الأمر /start
    app.add_handler(CommandHandler("start", start))
    
    # بدء استقبال التحديثات
    logger.info("✅ البوت بدأ العمل...")
    app.run_polling()

if __name__ == "__main__":
    # تشغيل البوت في خلفية منفصلة
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True   # يسمح بإيقاف الخيط عند إغلاق البرنامج الرئيسي
    bot_thread.start()
    
    # تشغيل خادم Flask على المنفذ الذي يحدده Render
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 خادم Flask يعمل على المنفذ {port}")
    app_flask.run(host="0.0.0.0", port=port)