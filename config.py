from dotenv import load_dotenv
import os
import threading
import asyncio
#import streamlit as st

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(dotenv_path="/workspaces/TG_bot1/.env")

#load_dotenv()

# Helper to retrieve environment variables
def get_token():
    hosting = os.getenv("HOSTING", "No Environment Variable Found")
    token = os.getenv("TOKEN", "No Token Found")
    print(f"HOSTING: {hosting}, TOKEN: {token}")  # Debug output
    if hosting == "replit":
        return token
    elif hosting == "streamlit":
        return token
    else:
        raise RuntimeError(f"Invalid or missing HOSTING environment variable! Current value: {hosting}")


# Helper to run the bot
def run_asyncio_bot(application):
    hosting = os.getenv("HOSTING", "No Environment Variable Found")
    if hosting == "replit":
        asyncio.run(application.run_polling(allowed_updates=["message"]))
    elif hosting == "streamlit":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread = threading.Thread(
            target=loop.run_until_complete,
            args=(application.run_polling(allowed_updates=["message"]),),
            daemon=True
        )
        thread.start()
    else:
        raise RuntimeError(f"Unsupported hosting configuration. Current value: {hosting}")