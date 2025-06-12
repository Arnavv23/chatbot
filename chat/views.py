import os
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from dotenv import load_dotenv
import configparser
from google import genai
import time
import random
import requests

# # Load environment variables from .env
# load_dotenv()
# api_key = os.getenv("NEXT_PUBLIC_GEMINI_API_KEY")
# print("Loaded Gemini API Key:", api_key)

# config = configparser.ConfigParser()
# config.read(f'C:\Users\Arnav\OneDrive\Desktop\chatbot_int\chatbot\chat\config.ini')
# api_key = config['API']['NEXT_PUBLIC_GEMINI_API_KEY']
# print(api_key)

api_key = 'AIzaSyAH8k7VSGMqCE8p25NfkBJmC4dFJlhQFoE'

def chat_view(request):
    return render(request, 'chatbot.html')

client = genai.Client(api_key=api_key)

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"response": "Please enter a message."})

            if not api_key:
                return JsonResponse({"response": "API key not configured."}, status=500)

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

            headers = {
                "Content-Type": "application/json"
            }

            # Updated prompt for Cyber SRC chatbot
            enhanced_prompt = f"""
You are Cyber SRC's official AI Cyber Security Assistant chatbot. Your job is to assist users with accurate, expert-level answers to cyber security-related questions. Respond clearly, concisely, and helpfully. Use step-by-step explanations when needed, and include relevant tools, best practices, real-world examples, and up-to-date terminology. You should know that the SRC in the company name stands for security risk complains

User query:
{user_message}
"""

            request_body = {
                "contents": [
                    {
                        "parts": [
                            {"text": enhanced_prompt}
                        ]
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=request_body)
            response.raise_for_status()

            result = response.json()
            print("API response:", result)

            generated_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't generate a response.")

            return JsonResponse({"response": generated_text})

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JsonResponse({"response": "Error from API: " + str(http_err)}, status=500)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"response": "Internal server error."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

def call_gemini_api(url, headers, payload, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 503:
                wait = (2 ** attempt) + random.uniform(0.5, 1.5)
                print(f"503 Error - retrying in {wait:.2f}s...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Gemini API is unavailable after several retries.")


# Create your views here.




# Create your views here.
