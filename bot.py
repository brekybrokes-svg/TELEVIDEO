import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
import yt_dlp

# Token'ı environment variable'dan al
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Merhaba! Ben video indirme botuyum. Bana YouTube, Instagram veya TikTok linki gönder, videoyu indirip sana göndereyim.")

def download_video(url: str) -> str:
    output_path = "downloaded_video.mp4"
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    if not user_message.startswith(('http://', 'https://')):
        update.message.reply_text("Lütfen geçerli bir URL gönderin.")
        return

    update.message.reply_text("Videoyu indiriyorum... ⏳")

    try:
        video_path = download_video(user_message)
        update.message.reply_video(video=open(video_path, 'rb'))
        os.remove(video_path)
    except Exception as e:
        logger.error(f"Hata: {e}")
        update.message.reply_text("❌ Video indirilemedi. URL'yi kontrol edin veya daha sonra tekrar deneyin.")

def main():
    # use_context parametresini kaldırın
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

