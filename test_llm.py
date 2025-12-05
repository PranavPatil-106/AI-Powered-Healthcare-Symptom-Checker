from backend.llm_service import analyze_symptoms
import os
from dotenv import load_dotenv

load_dotenv()

print(f"Testing LLM with Key: {os.getenv('GEMINI_API_KEY')[:5]}...")

try:
    result = analyze_symptoms("I have a headache and fever.")
    print("LLM Response:")
    print(result)
except Exception as e:
    print(f"LLM Failed: {e}")
