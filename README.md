# AI Powered Healthcare Symptom Checker 🩺

An intelligent symptom checker application that uses Google's Gemini AI to analyze symptoms and provide probable conditions, precautions, severity levels, and medical advice. Built with FastAPI, Streamlit, and MySQL.

## ✨ Features

-   **AI-Powered Analysis**: Uses Gemini Flash to analyze symptoms in natural language.
-   **Severity Assessment**: Automatically categorizes symptoms as Low, Moderate, or High severity.
-   **Secure Authentication**: User signup and login with JWT-based authentication and password hashing.
-   **History Tracking**: Saves all symptom checks with filtering (by severity) and sorting (by date) capabilities.
-   **User-Friendly UI**: Clean, modern interface built with Streamlit, featuring a sidebar for easy navigation and healthy tips.
-   **Responsive Design**: Works seamlessly on desktop and mobile browsers.

## 🛠️ Tech Stack

-   **Frontend**: Streamlit (Python)
-   **Backend**: FastAPI (Python)
-   **Database**: MySQL
-   **AI Model**: Google Gemini (via LangChain)
-   **Authentication**: JWT (JSON Web Tokens) & Passlib (pbkdf2_sha256)

## 🚀 Setup Instructions

### Prerequisites

-   Python 3.8+
-   MySQL Server
-   Google Gemini API Key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-healthcare-symptom-checker
```

### 2. Create Virtual Environment

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

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/ai_healthcare_symptom_checker
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Database Setup

1.  Open MySQL Workbench or your preferred SQL client.
2.  Run the script located in `schema.sql` to create the database and tables.

### 6. Run the Application

**Start the Backend Server:**

```bash
cd backend
uvicorn main:app --reload
```

**Start the Frontend Application:**

Open a new terminal, activate the venv, and run:

```bash
streamlit run frontend/app.py
```

## 📝 Usage

1.  **Sign Up**: Create a new account with your username, email, and password.
2.  **Login**: Access your account.
3.  **Check Symptoms**: Enter your symptoms in the text box and click "Check Symptoms".
4.  **View Results**: Read the AI's analysis, including probable conditions, precautions, and severity level.
5.  **History**: View your past checks in the "History" tab. Filter by severity or sort by date.

## ⚠️ Disclaimer

This tool is for **educational purposes only** and does not replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
