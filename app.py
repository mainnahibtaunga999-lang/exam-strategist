import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. App Configuration
st.set_page_config(page_title="Exam Gap Strategist", page_icon="📅")
st.title("📅 The Gap-Day Strategist")
st.write("Upload your Exam Date Sheet, and I'll build the perfect study plan for your gap days.")

# 2. Get the API Key safely
try:
    # Try getting it from Secrets (for the website)
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # Fallback for local testing (optional)
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Main Inputs (Simple & Clean)
uploaded_file = st.file_uploader("📸 Upload a photo of your Date Sheet", type=["jpg", "png", "jpeg"])
syllabus_text = st.text_area("📝 Paste your Syllabus (or Chapter list)", height=150, placeholder="Example: Math: Ch 1-10, Science: Ch 5-8...")

# 4. The "Magic" Button
if st.button("🚀 Generate My Strategy"):
    if not uploaded_file:
        st.error("Please upload your Date Sheet image.")
    elif not syllabus_text:
        st.error("Please enter your syllabus.")
    else:
        with st.spinner("Analyzing your exam dates... (This takes about 10 seconds)"):
            try:
                # Use the Flash model
                model = genai.GenerativeModel('gemini-1.5-flash')
                image = Image.open(uploaded_file)

                # The Prompt
                prompt = f"""
                You are an expert exam strategist for a student. 
                1. Look at the uploaded image of the Date Sheet. Identify the dates and subjects.
                2. Look at the syllabus provided here: {syllabus_text}
                3. Calculate the 'Gap Days' (holidays) between each exam.
                4. Create a STRICT hour-by-hour study plan for those gap days.
                5. Rules: 
                   - Prioritize hard chapters for the first half of the gap.
                   - Keep the last day before the exam for revision only.
                   - Be encouraging but strict.
                6. Output the plan in a clean, easy-to-read format.
                """

                # Get the response
                response = model.generate_content([prompt, image])
                st.success("Plan Generated! Scroll down 👇")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
