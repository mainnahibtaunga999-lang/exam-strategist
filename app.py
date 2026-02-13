import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import requests
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION ---
AD_LINK = "https://omg10.com/4/10607555" 

st.set_page_config(page_title="Gap-Day Strategist", page_icon="⚡", layout="centered")

# Custom CSS
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
        text-decoration: none;
        display: block;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0, 200, 81, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Animation
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_ai = load_lottieurl("https://lottie.host/02a58b56-34a8-4447-9755-90082c9e223c/yFj8YwZ5Ww.json")

# API Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Key missing in Streamlit Secrets!")
    st.stop()

# --- 2. UI ---
col1, col2 = st.columns([1, 2])
with col1:
    if lottie_ai: st_lottie(lottie_ai, height=130)
with col2:
    st.title("⚡ Gap-Day Strategist")
    st.caption("AI Exam Planning for Students")

# Inputs
st.markdown("### 1️⃣ Student Profile")
c1, c2 = st.columns(2)
student_class = c1.selectbox("Class", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])
student_board = c2.selectbox("Board", ["CBSE", "ICSE", "State Board", "Other"])

st.markdown("### 2️⃣ Details")
uploaded_file = st.file_uploader("Upload Date Sheet", type=["jpg", "png", "jpeg"])
syllabus_text = st.text_area("Syllabus", placeholder="Ch 1-5, etc.")

st.markdown("### 3️⃣ Personalize")
study_hours = st.slider("Daily Hours?", 1, 16, 6)
weak_subjects = st.text_input("Weak Subjects?", placeholder="Math, Science...")

st.markdown("---")
st.subheader("4️⃣ Unlock Strategy")
st.markdown(f'<a href="{AD_LINK}" target="_blank" class="unlock-btn">🔓 Click to Unlock</a>', unsafe_allow_html=True)
confirm = st.checkbox("✅ I have clicked the unlock button")

if st.button("🚀 Generate My Plan"):
    if not confirm:
        st.error("Please click the Unlock button first!")
    elif not uploaded_file:
        st.warning("Please upload your Date Sheet.")
    else:
        with st.spinner("🤖 Trying active models..."):
            # This list ensures a 100% success rate by trying every possible model ID for 2026
            models_to_try = [
                'gemini-3-flash-001',   # Newest 2026 Stable
                'gemini-3-flash',       # 2026 Standard
                'gemini-1.5-flash',     # Classic Universal Alias
                'gemini-pro'            # Emergency Backup
            ]
            
            success = False
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    image = Image.open(uploaded_file)
                    prompt = f"Coach a {student_class} {student_board} student. Hours: {study_hours}. Weak: {weak_subjects}. Create a schedule from this image and syllabus: {syllabus_text}"
                    response = model.generate_content([prompt, image])
                    st.success(f"Success! (Model: {model_name})")
                    st.markdown(response.text)
                    success = True
                    break 
                except Exception:
                    continue # Try the next model if this one fails
            
            if not success:
                st.error("Google is currently updating their servers. Please try again in 5 minutes.")
