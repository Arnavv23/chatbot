from google import genai
import requests


YOUR_API_KEY = 'AIzaSyAH8k7VSGMqCE8p25NfkBJmC4dFJlhQFoE'

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
