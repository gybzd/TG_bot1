from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Retrieve secrets
api_key = os.getenv("API_KEY", "No API Key Found")
db_password = os.getenv("DB_PASSWORD", "No DB Password Found")
zalupa1 = os.getenv("zalupa1", "No Environment Variable Found")

# Display secrets for testing (avoid in production)
st.write("API Key:", api_key)
st.write("DB Password:", db_password)
st.write("zalupa1:", zalupa1)
