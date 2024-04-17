from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import os

app = Flask(__name__)
TOKEN = os.getenv('TOKEN')  # Load the token from environment variables
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

@app.route('/')
def hello_world():
    return 'Hello, this is my Telegram bot running on Glitch!'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == '__main__':
    app.run(port=3000)  # Glitch exposes applications on port 3000 by default
