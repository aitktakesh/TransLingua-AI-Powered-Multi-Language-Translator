import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello, can you hear me?")
    print("SUCCESS")
    print(response.text)
except Exception as e:
    print(f"ERROR: {e}")
