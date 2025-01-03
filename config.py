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

# helper to retrieve DB variables
def get_database_url():
    hosting = os.getenv("HOSTING", "No Environment Variable Found")
    db_path = os.getenv("DB_PATH", "sqlite:///./default.db")
    print(f"HOSTING: {hosting}, DB_PATH: {db_path}")  # Debug output
    if hosting == "streamlit":
        return db_path  # SQLite database path
    else:
        raise RuntimeError(f"Invalid or missing HOSTING environment variable for database! Current value: {hosting}")

# Helper to run the bot
def run_asyncio_bot(application):
    hosting = os.getenv("HOSTING", "No Environment Variable Found")
    if hosting == "replit":
        asyncio.run(application.run_polling(allowed_updates=["message"]))
    elif hosting == "streamlit":
        # For Streamlit, run the bot in a separate thread without signal handlers
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def start_polling():
            await application.initialize()  # Initialize the bot
            await application.start()       # Start the bot
            try:
                await application.updater.start_polling(allowed_updates=["message"])
                await asyncio.Event().wait()  # Keep the loop running
            finally:
                await application.updater.stop()
                await application.stop()
                await application.shutdown()

        # Threaded execution
        thread = threading.Thread(
            target=lambda: loop.run_until_complete(start_polling()),
            daemon=True
        )
        thread.start()
    else:
        raise RuntimeError(f"Unsupported hosting configuration. Current value: {hosting}")