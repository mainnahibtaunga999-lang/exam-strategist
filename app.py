import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# --- CONFIGURATION ---
AD_LINK = "https://omg10.com/4/10607555" 

st.set_page_config(page_title="Gap-Day Strategist", page_icon="⚡", layout="centered")

# --- DEBUG: CHECK API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # Show first 4 chars to verify it's reading correctly (Safe to show)
    st.write(f"🔑 Debug: Key loaded? Yes. Starts with: {api_key[:4]}...")
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"⚠️ Critical Secret Error: {e}")
    st.stop()

# --- UI SETUP ---
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

st.title("⚡ Gap-Day Strategist (Debug Mode)")

# --- UNLOCK SECTION ---
if not st.session_state.unlocked:
    st.info("Click to Unlock")
    if st.button("🔓 CLICK TO UNLOCK"):
        st.session_state.unlocked = True
        js_code = f'window.open("{AD_LINK}", "_blank");'
        components.html(f'<script>{js_code}</script>', height=0)
        st.rerun()

# --- MAIN APP ---
else:
    st.success("✅ App Unlocked")
    
    uploaded_file = st.file_uploader("Upload Date Sheet", type=["jpg", "png", "jpeg"])
    syllabus_text = st.text_area("Syllabus")

    if st.button("🚀 Generate Plan"):
        if not uploaded_file:
            st.warning("Upload image first.")
        else:
            with st.spinner("Connecting to Google AI..."):
                try:
                    # USING THE STANDARD MODEL ONLY
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    image = Image.open(uploaded_file)
                    prompt = f"Analyze this date sheet. Syllabus: {syllabus_text}. Create a study plan."
                    
                    response = model.generate_content([prompt, image])
                    st.markdown(response.text)
                    
                except Exception as e:
                    # THIS WILL PRINT THE REAL ERROR
                    st.error("❌ CONNECTION ERROR:")
                    st.error(e)
                    st.code(f"Error Details: {str(e)}")
