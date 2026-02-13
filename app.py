import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
AD_LINK = "https://omg10.com/4/10607555" 

st.set_page_config(page_title="Gap-Day Strategist", page_icon="⚡", layout="centered")

# Initialize "Unlocked" state
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# Custom CSS for Premium Look
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .unlock-btn {
        background: linear-gradient(45deg, #00C851, #007E33);
        color: white !important;
        padding: 16px 32px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        display: block;
        margin: 20px 0;
        cursor: pointer;
        border: none;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 200, 81, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Animation Helper
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_ai = load_lottieurl("https://lottie.host/02a58b56-34a8-4447-9755-90082c9e223c/yFj8YwZ5Ww.json")

# API Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Key missing in Secrets!")
    st.stop()

# --- 2. THE UI ---
col1, col2 = st.columns([1, 2])
with col1:
    if lottie_ai: st_lottie(lottie_ai, height=130)
with col2:
    st.title("⚡ Gap-Day Strategist")
    st.caption("AI-Powered Exam Planning for Students")

# --- STEP 1: THE LOCK ---
if not st.session_state.unlocked:
    st.subheader("🔓 Unlock the AI")
    st.info("To keep this tool free, click the button below to view a quick ad and unlock the generator.")
    
    if st.button("🔓 CLICK TO UNLOCK", key="main_unlock_btn"):
        # This is the magic part:
        # 1. It flips the switch in the background
        st.session_state.unlocked = True
        # 2. It uses Javascript to open your Monetag link in a new tab
        js_code = f'window.open("{AD_LINK}", "_blank");'
        components.html(f'<script>{js_code}</script>', height=0)
        st.rerun() # Refresh to show the app

# --- STEP 2: THE APP (Only shows after unlock) ---
else:
    st.success("✅ App Unlocked! You can now generate your plan.")
    
    st.markdown("### 1️⃣ Student Profile")
    c1, c2 = st.columns(2)
    student_class = c1.selectbox("Select Class", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])
    student_board = c2.selectbox("Select Board", ["CBSE", "ICSE", "State Board", "Other"])

    st.markdown("### 2️⃣ Exam Details")
    uploaded_file = st.file_uploader("Upload Date Sheet (Image)", type=["jpg", "png", "jpeg"])
    syllabus_text = st.text_area("Syllabus / Chapter List", placeholder="Math: Ch 1-5, Physics: Ch 2...")

    st.markdown("### 3️⃣ Personalize")
    study_hours = st.slider("Daily Study Hours?", 1, 16, 6)
    weak_subjects = st.text_input("Weak Subjects?", placeholder="e.g. Math, Physics")

    if st.button("🚀 Generate My Plan"):
        if not uploaded_file or not syllabus_text:
            st.warning("Please upload your Date Sheet and Syllabus first.")
        else:
            with st.spinner("🤖 Trying active AI models..."):
                # Self-Healing Model List for 2026
                models_to_try = [
                    'gemini-3-flash-001', 
                    'gemini-3-flash', 
                    'gemini-1.5-flash', 
                    'gemini-pro'
                ]
                
                success = False
                for m_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(m_name)
                        image = Image.open(uploaded_file)
                        prompt = f"Coach a {student_class} {student_board} student. {study_hours} hrs/day. Weak: {weak_subjects}. Plan using image & syllabus: {syllabus_text}"
                        response = model.generate_content([prompt, image])
                        st.balloons()
                        st.markdown(response.text)
                        success = True
                        break 
                    except:
                        continue
                
                if not success:
                    st.error("Server busy. Please try again in 2 minutes.")
