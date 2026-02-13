import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
# Replace with your Monetag Link
AD_LINK = "https://omg10.com/4/10607555" 

st.set_page_config(page_title="Gap-Day Strategist", page_icon="⚡", layout="centered")

# Initialize "Unlocked" state
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# Premium CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .unlock-btn {
        background: linear-gradient(45deg, #00C851, #007E33);
        color: white !important;
        padding: 18px 32px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        display: block;
        margin: 20px 0;
        cursor: pointer;
        border: none;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 200, 81, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# API Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Key missing in Secrets!")
    st.stop()

# --- 2. THE UI ---
st.title("⚡ Gap-Day Strategist")
st.caption("Class 9 Exam Planner (Tikamgarh Edition)")

# --- STEP 1: THE LOCK ---
if not st.session_state.unlocked:
    st.subheader("🔓 Unlock the Generator")
    st.info("This tool is free. Click below to view a quick ad and unlock the AI planner.")
    
    if st.button("🔓 CLICK TO UNLOCK", key="main_unlock_btn"):
        st.session_state.unlocked = True
        # JavaScript opens the ad and tells Streamlit to show the app
        js_code = f'window.open("{AD_LINK}", "_blank");'
        components.html(f'<script>{js_code}</script>', height=0)
        st.rerun() 

# --- STEP 2: THE MAIN APP (Hidden until Unlock) ---
else:
    st.success("✅ Access Granted! Upload your date sheet below.")
    
    c1, c2 = st.columns(2)
    with c1:
        student_class = st.selectbox("Class", ["Class 9", "Class 10"])
    with c2:
        study_hours = st.slider("Daily Hours?", 1, 12, 6)

    uploaded_file = st.file_uploader("Upload Date Sheet Photo", type=["jpg", "png", "jpeg"])
    syllabus = st.text_area("List your chapters (e.g., Physics Ch 1-3)")

    if st.button("🚀 Generate My Plan"):
        if not uploaded_file:
            st.warning("Please upload a photo of your date sheet.")
        else:
            with st.spinner("🤖 AI is reading your schedule..."):
                # 2026 Model Fallback List
                models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                success = False
                
                for m_name in models:
                    try:
                        model = genai.GenerativeModel(m_name)
                        img = Image.open(uploaded_file)
                        prompt = f"Student: {student_class}. Study: {study_hours}h/day. Syllabus: {syllabus}. Create a plan from this date sheet."
                        response = model.generate_content([prompt, img])
                        st.balloons()
                        st.markdown(response.text)
                        success = True
                        break 
                    except Exception:
                        continue # Try the next name if Google gives a 404
                
                if not success:
                    st.error("Google's servers are updating. Please try again in 5 minutes.")
