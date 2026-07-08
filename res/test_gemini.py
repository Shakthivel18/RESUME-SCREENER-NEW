import google.generativeai as genai
import os

key = os.getenv('GEMINI_API_KEY', 'AIzaSyBhtaBQg32BewYjN9y-JfQxMVLJDqxedl8')
genai.configure(api_key=key)

models_to_test = [
    'gemini-2.0-flash', 
    'gemini-1.5-flash', 
    'gemini-1.5-flash-8b', 
    'gemini-1.5-pro',
    'gemini-pro'
]

for m in models_to_test:
    print(f"\nTesting {m}...")
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("hello")
        print(f"SUCCESS: {m}")
        print(response.text)
    except Exception as e:
        print(f"FAILED: {m} - {e}")
