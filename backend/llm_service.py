import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=GEMINI_API_KEY)

template = """
You are a helpful medical assistant. Your goal is to provide educational information based on the symptoms provided.
Use simple, clear language that is easy for a person without medical knowledge to understand. Avoid complex medical jargon, or explain it simply if necessary.

Symptoms: {symptoms}

Please provide your response in the following strict format. Do not include any introductory or concluding text. Use Markdown for formatting.

Severity Level: [Low/Moderate/High]

### 1. Probable Conditions:
* **[Condition Name]:** [Brief description]
* **[Condition Name]:** [Brief description]

### 2. Precautions:
* **[Precaution]:** [Brief description]
* **[Precaution]:** [Brief description]

### 3. When to consult doctor:
* **[Warning Sign]:** [Brief description]
* **[Warning Sign]:** [Brief description]

Response:
"""

prompt = PromptTemplate(
    input_variables=["symptoms"],
    template=template,
)

chain = prompt | llm

def analyze_symptoms(symptoms: str) -> dict:
    try:
        response = chain.invoke({"symptoms": symptoms})
        content = response.content
        text_content = ""
        
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                elif isinstance(item, str):
                    text_parts.append(item)
                else:
                    text_parts.append(str(item))
            text_content = " ".join(text_parts)
        else:
            text_content = str(content)
            
        # Extract Severity
        severity = "Unknown"
        if "Severity Level:" in text_content:
            try:
                parts = text_content.split("Severity Level:")
                if len(parts) > 1:
                    # The part after "Severity Level:" contains the level and the rest of the text
                    # We need to isolate the level (first line)
                    rest_of_text = parts[1].strip()
                    severity_line = rest_of_text.split("\n")[0]
                    
                    severity_part = severity_line.replace("*", "").replace("[", "").replace("]", "").strip()
                    if "Low" in severity_part: severity = "Low"
                    elif "Moderate" in severity_part: severity = "Moderate"
                    elif "High" in severity_part: severity = "High"
                    
                    # Remove the Severity line from the text content to avoid duplication/clutter
                    # We reconstruct the text without the "Severity Level: ..." line
                    text_content = text_content.replace(f"Severity Level: {severity_line}", "").strip()
            except:
                pass
        
        return {"result": text_content, "severity": severity}

    except Exception as e:
        return {"result": f"Error analyzing symptoms: {str(e)}", "severity": "Error"}
