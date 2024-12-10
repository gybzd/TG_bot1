#!/usr/bin/env python
import logging
import threading
import asyncio
import os
from telegram import __version__ as TG_VER, ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont

# Check Telegram version compatibility
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(f"Current PTB version {TG_VER} is not supported.")

# Get bot token
TOKEN = os.environ.get('TOKEN', None)
if not TOKEN:
    raise RuntimeError("Telegram bot token not set. Please set 'TOKEN' as an environment variable.")

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

async def stylize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if not user_message:
        await update.message.reply_text("Please send text to stylize.")
        return

    img = Image.new('RGB', (500, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    fnt = ImageFont.load_default()
    d.text((50, 90), user_message, font=fnt, fill=(255, 255, 0))

    img.save('styled_text.png')
    with open('styled_text.png', 'rb') as photo:
        await update.message.reply_photo(photo=photo)

# Function to start the bot
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))

    # Run the event loop explicitly
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.run_polling(allowed_updates=Update.ALL_TYPES))

# Main function
def main():
    # Start bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Bot started in a separate thread.")

    # Placeholder for main app (e.g., Streamlit UI)
    print("Main application running. Bot is live.")

if __name__ == "__main__":
    main()
