import streamlit as st
from api_client import APIClient
import time

# Initialize API Client
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient()

if 'token' not in st.session_state:
    st.session_state.token = None

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

def login_page():
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
    
    if submitted:
        with st.spinner("Logging in..."):
            result = st.session_state.api_client.login(email, password)
            if "access_token" in result:
                st.session_state.token = result["access_token"]
                st.session_state.api_client.set_token(result["access_token"])
                st.session_state.username = result.get("username", email)
                st.success(f"Logged in as {st.session_state.username}")
                st.rerun()
            else:
                st.error(result.get("error", "Login failed"))

def signup_page():
    st.title("Sign Up")
    with st.form("signup_form"):
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password", help="Minimum 8 characters")
        submitted = st.form_submit_button("Sign Up")
    
    if submitted:
        if len(password) < 8:
            st.error("Password must be at least 8 characters long")
        else:
            with st.spinner("Signing up..."):
                result = st.session_state.api_client.signup(username, email, password)
                if "access_token" in result:
                    st.session_state.token = result["access_token"]
                    st.session_state.api_client.set_token(result["access_token"])
                    st.session_state.username = result.get("username", username)
                    st.success(f"Account created! Welcome {st.session_state.username}")
                    st.rerun()
                else:
                    st.error(result.get("error", "Signup failed"))

import random
from datetime import datetime

HEALTHY_TIPS = [
    "Drink at least 8 glasses of water a day to stay hydrated.",
    "Aim for 7-9 hours of sleep each night for optimal health.",
    "Incorporate fruits and vegetables into every meal.",
    "Take a 30-minute walk daily to improve cardiovascular health.",
    "Practice deep breathing exercises to reduce stress.",
    "Wash your hands frequently to prevent the spread of germs.",
    "Limit processed sugar intake for better energy levels.",
    "Stretch daily to improve flexibility and prevent injury.",
    "Take breaks from screens every 20 minutes to reduce eye strain.",
    "Stay socially connected to boost mental well-being."
]

def format_date(date_str):
    try:
        # Assuming date_str is in ISO format or similar from DB
        # Adjust format if needed based on actual DB output
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return date_str

def main_page():
    # Sidebar Content
    st.sidebar.markdown(f"### 👋 Welcome, **{st.session_state.get('username', 'User')}**!")
    
    # Random Healthy Tip in Sidebar
    if "daily_tip" not in st.session_state:
        st.session_state.daily_tip = random.choice(HEALTHY_TIPS)
    
    st.sidebar.info(f"💡 **Healthy Tip:**\n\n{st.session_state.daily_tip}")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", key="logout_sidebar"):
        st.session_state.token = None
        st.session_state.username = None
        if "daily_tip" in st.session_state:
            del st.session_state["daily_tip"]
        st.rerun()

    # Main Content
    tab1, tab2 = st.tabs(["Symptom Checker", "History"])

    with tab1:
        st.title("AI Symptom Checker")
        st.markdown("""
        **Process:**
        1. Enter your symptoms in the text area below.
        2. Click "Check Symptoms".
        3. Review the probable conditions and recommendations.
        
        > **Disclaimer:** This tool is for educational purposes only and does not replace professional medical advice.
        """)
        
        with st.form(key="symptom_form"):
            symptoms = st.text_area("Describe your symptoms here...", height=150, key="symptoms_input")
            submit_button = st.form_submit_button(label="Check Symptoms")
        
        if submit_button:
            if symptoms:
                with st.spinner("Analyzing..."):
                    result = st.session_state.api_client.analyze_symptoms(symptoms)
                    if "result" in result:
                        st.markdown("### Analysis Result")
                        
                        # Display Severity Badge
                        severity = result.get("severity", "Unknown")
                        severity_color = "gray"
                        if severity == "Low": severity_color = "green"
                        elif severity == "Moderate": severity_color = "orange"
                        elif severity == "High": severity_color = "red"
                        
                        st.markdown(f"**Severity Level:** :{severity_color}[{severity}]")
                        st.write(result["result"])
                    else:
                        st.error(result.get("error", "Analysis failed"))
            else:
                st.warning("Please enter some symptoms.")

    with tab2:
        st.title("Your History")
        
        # Filters
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            severity_filter = st.selectbox("Filter by Severity", ["All", "Low", "Moderate", "High"])
        with col_filter2:
            sort_order = st.selectbox("Sort by Date", ["Newest First", "Oldest First"])

        with st.spinner("Loading history..."):
            history = st.session_state.api_client.get_history()
            if isinstance(history, list):
                if not history:
                    st.info("No history found.")
                
                # Apply Sorting
                if sort_order == "Oldest First":
                    history.sort(key=lambda x: x['created_at'])
                else:
                    history.sort(key=lambda x: x['created_at'], reverse=True)
                
                # Apply Filtering
                filtered_history = []
                for item in history:
                    item_severity = item.get('severity', 'Unknown')
                    if severity_filter == "All" or (item_severity and severity_filter.lower() in item_severity.lower()):
                        filtered_history.append(item)
                
                if not filtered_history:
                    st.info("No history matches your filter.")

                for item in filtered_history:
                    date_display = format_date(item['created_at'])
                    symptom_preview = item['symptoms'][:40] + "..." if len(item['symptoms']) > 40 else item['symptoms']
                    severity_display = item.get('severity', 'Unknown')
                    
                    # Color code severity
                    severity_color = "gray"
                    if severity_display == "Low": severity_color = "green"
                    elif severity_display == "Moderate": severity_color = "orange"
                    elif severity_display == "High": severity_color = "red"

                    with st.expander(f"📅 {date_display} - {symptom_preview}"):
                        if severity_display and severity_display != "Unknown":
                            st.markdown(f"**Severity:** :{severity_color}[{severity_display}]")
                        st.markdown(f"**Symptoms:** {item['symptoms']}")
                        st.markdown("---")
                        st.markdown(f"**Analysis:**\n{item['result']}")
            else:
                st.error(history.get("error", "Failed to load history"))

def main():
    st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺", layout="wide")
    
    if st.session_state.token:
        main_page()
    else:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login_page()
        with tab2:
            signup_page()

if __name__ == "__main__":
    main()
