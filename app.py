#!/usr/bin/env python
import logging
from telegram import __version__ as TG_VER, ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont
from config import get_token, run_asyncio_bot

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
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

def main():
    """Start the bot."""
    TOKEN = get_token()
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))

    # Start the bot based on hosting
    run_asyncio_bot(application)

if __name__ == "__main__":
    main()
