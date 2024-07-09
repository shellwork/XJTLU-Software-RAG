import os
from openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key: {api_key}")

if api_key is None:
    print("API key is not set")
else:
    client = OpenAI(api_key=api_key)
    print("OpenAI client initialized successfully")
