# Healthcare Symptom Checker 🩺

Welcome to the **Healthcare Symptom Checker**, an AI-powered application designed to provide preliminary medical insights based on user-reported symptoms. This project demonstrates the integration of a modern web frontend, a robust backend API, and a Large Language Model (LLM) to deliver educational health information.

## 🎯 Objective

The primary goal of this system is to bridge the gap between initial symptom onset and medical consultation. By inputting symptoms in natural language, users receive:
1.  **Probable Conditions**: A list of potential causes for the symptoms.
2.  **Recommendations**: Suggested next steps and precautions.
3.  **Severity Assessment**: An AI-generated estimation of urgency (Low, Moderate, High).

> **Disclaimer**: This tool is for **educational purposes only** and does not replace professional medical advice.

## 📋 Scope of Work

This project fulfills the requirements of **Healthcare Symptom Checker**, covering:
*   **Input**: User-friendly text interface for describing symptoms.
*   **Output**: Structured response containing conditions, precautions, and when to see a doctor.
*   **Interface**: A full-stack web application with a dedicated frontend form.

## 🏛️ Technical Architecture

I designed this application with a modular architecture to ensure scalability and maintainability:

*   **Frontend**: Built with **Streamlit** for a responsive and interactive user interface.
*   **Backend**: Developed using **FastAPI** to handle requests, manage user sessions, and route API calls.
*   **Database**: **MySQL** is used to securely store user profiles and symptom history.
*   **LLM Integration**: **Google Gemini (Flash)** via LangChain provides the reasoning engine for symptom analysis.

### Tech Stack
*   **Language**: Python 3.9+
*   **Frameworks**: FastAPI, Streamlit
*   **AI/ML**: LangChain, Google Gemini API
*   **Database**: MySQL, SQLAlchemy (ORM)
*   **Authentication**: JWT (JSON Web Tokens) with Passlib

## 🚀 Setup & Installation

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone <repository_url>
cd healthcare-symptom-checker
```

### 2. Set Up Virtual Environment
It is recommended to use a virtual environment.
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your credentials:
```env
DATABASE_URL=mysql+mysqlconnector://<user>:<password>@localhost:3306/<database_name>
GEMINI_API_KEY=your_google_gemini_api_key
SECRET_KEY=your_secure_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Initialize Database
Ensure your MySQL server is running, then create the schema:
```bash
# You can run the provided schema.sql in your MySQL client
source schema.sql
```

### 6. Run the Application
You will need two terminal windows.

**Terminal 1: Backend**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2: Frontend**
```bash
streamlit run frontend/app.py
```

## 💡 Usage Guide

1.  **Register/Login**: Securely create an account to save your history.
2.  **Describe Symptoms**: Enter details like "I have a throbbing headache and sensitivity to light."
3.  **Get Results**: The AI analyzes the text and prompts: *"Based on these symptoms, suggest possible conditions and next steps with educational disclaimer."*
4.  **View History**: Check past analyses filtered by severity level.

## 🛡️ Safety & Reliability

*   **Data Privacy**: Passwords are hashed before storage.
*   **Content Safety**: The LLM is prompted to always include medical disclaimers and avoid definitive diagnoses.
*   **Error Handling**: graceful degradation if the AI service is unavailable.

