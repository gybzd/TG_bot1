from dotenv import load_dotenv
import os
import threading
import asyncio
import streamlit as st

# Helper to retrieve environment variables
def get_token():
    if os.environ.get("HOSTING") == "replit":
        return os.environ["TOKEN"]
    elif os.getenv("HOSTING") == "streamlit":
        return st.secrets["TOKEN"]
    else:
        raise RuntimeError("HOSTING environment variable not set or invalid!")

# Helper to run the bot
def run_asyncio_bot(application):
    if os.environ.get("HOSTING") == "replit":
        asyncio.run(application.run_polling(allowed_updates=["message"]))
    elif os.environ.get("HOSTING") == "streamlit":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread = threading.Thread(target=loop.run_until_complete, args=(application.run_polling(allowed_updates=["message"]),), daemon=True)
        thread.start()
    else:
        raise RuntimeError("Unsupported hosting configuration.")
