import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "8465954340:AAF0effLI9fPqCX0B64ynhrOS8Rtde6WywE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben video indirme botuyum. Bana YouTube, Instagram veya TikTok linki gönder, videoyu indirip sana göndereyim.")

def download_video(url: str) -> str:
    output_path = "downloaded_video.mp4"
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message.startswith(('http://', 'https://')):
        await update.message.reply_text("Lütfen geçerli bir URL gönderin.")
        return

    await update.message.reply_text("Videoyu indiriyorum... ⏳")

    try:
        video_path = download_video(user_message)
        await update.message.reply_video(video=open(video_path, 'rb'))
        os.remove(video_path)
    except Exception as e:
        logger.error(f"Hata: {e}")
        await update.message.reply_text("❌ Video indirilemedi. URL'yi kontrol edin veya daha sonra tekrar deneyin.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()