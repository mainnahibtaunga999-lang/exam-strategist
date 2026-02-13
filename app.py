import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import requests
from streamlit_lottie import st_lottie

# --- 1. PASTE YOUR DIRECT LINK HERE ---
# (Keep the quotes "" around it!)
AD_LINK = "https://omg10.com/4/10607555" 

# --- 2. APP CONFIGURATION ---
st.set_page_config(page_title="Gap-Day Strategist", page_icon="⚡", layout="centered")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    
    /* The UNLOCK Button - Green & Glowing */
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
        transition: transform 0.2s;
    }
    .unlock-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 200, 81, 0.6);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: #262730;
        color: white; 
        border: 1px solid #41444e;
    }
</style>
""", unsafe_allow_html=True)

# Helper for Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# Load Robot Animation
lottie_ai = load_lottieurl("https://lottie.host/02a58b56-34a8-4447-9755-90082c9e223c/yFj8YwZ5Ww.json")

# API Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Key missing! Check Streamlit Secrets.")
    st.stop()

# --- 3. THE UI ---
col1, col2 = st.columns([1, 2])
with col1:
    if lottie_ai: st_lottie(lottie_ai, height=130, key="ai_anim")
with col2:
    st.title("⚡ Gap-Day Strategist")
    st.caption("AI-Powered Exam Planner for Students")

# --- NEW SECTION: Student Profile ---
st.markdown("### 1️⃣ Student Profile")
col_class, col_board = st.columns(2)
with col_class:
    student_class = st.selectbox("Select Your Class", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
with col_board:
    student_board = st.selectbox("Select Your Board", ["CBSE", "ICSE", "State Board", "IB / IGCSE", "Other"])

# --- SECTION: Exam Details ---
st.markdown("### 2️⃣ Exam Details")
uploaded_file = st.file_uploader("Upload Date Sheet (Image)", type=["jpg", "png", "jpeg"])
syllabus_text = st.text_area("Syllabus / Chapter List", height=100, placeholder="Math: Ch 1-5, Physics: Ch 2...")

# --- SECTION: Personalize ---
st.markdown("### 3️⃣ Personalize It")
col_hours, col_grasp = st.columns(2)
with col_hours:
    study_hours = st.slider("Daily Study Hours?", 1, 16, 6)
with col_grasp:
    days_left = st.number_input("Days until exams start?", min_value=1, value=5)

weak_subjects = st.text_input("Which subjects are you WEAK in?", placeholder="e.g. Math, Physics")

st.markdown("---")

# --- 4. THE MONEY MAKER ---
st.subheader("4️⃣ Unlock Your Strategy")
st.info("View a quick ad to unlock the AI calculation.")

# The Ad Button
st.markdown(f'<a href="{AD_LINK}" target="_blank" class="unlock-btn">🔓 Click to Unlock</a>', unsafe_allow_html=True)

# The Verification Checkbox
confirm = st.checkbox("✅ I have clicked the unlock button")

if st.button("🚀 Generate My Plan"):
    if not confirm:
        st.error("Please click the Unlock button first to support the server!")
    elif not uploaded_file or not syllabus_text:
        st.warning("Please upload your Date Sheet and Syllabus first.")
    else:
        with st.spinner("🤖 Designing your perfect schedule..."):
            try:
                model = genai.GenerativeModel('gemini-3-flash')
                image = Image.open(uploaded_file)
                prompt = f"""
                Act as a strict exam coach for a {student_class} ({student_board} Board) student. 
                1. Analyze the Date Sheet image.
                2. Student Syllabus: {syllabus_text}
                3. Constraints:
                   - Can study {study_hours} hours per day.
                   - Exams start in {days_left} days.
                   - WEAK SUBJECTS (Focus more on these): {weak_subjects}
                
                4. Create a Gap-Day schedule.
                5. Rules:
                   - Allocate MORE hours to the 'Weak Subjects' mentioned.
                   - Break the {study_hours} hours into realistic sessions (e.g., 2 hours study, 15 min break).
                   - Be specific: Don't just say "Study Math", say "Math: Chapter 1 & 2".
                
                Format using Markdown with bold headers.
                """
                response = model.generate_content([prompt, image])
                
                st.balloons()
                st.success("Strategy Ready!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
