import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. App Title and Description
st.set_page_config(page_title="Exam Gap Strategist", page_icon="📅")
st.title("📅 The Gap-Day Strategist")
st.write("Upload your Exam Date Sheet, and I'll build the perfect study plan for your gap days.")

# 2. Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")
    st.markdown("[Get your free key here](https://aistudio.google.com/app/apikey)")

# 3. Main Inputs
uploaded_file = st.file_uploader("📸 Upload a photo of your Date Sheet", type=["jpg", "png", "jpeg"])
syllabus_text = st.text_area("📝 Paste your Syllabus (or Chapter list)", height=150, placeholder="Example: Math: Ch 1-10, Science: Ch 5-8...")

# 4. The "Magic" Button
if st.button("🚀 Generate My Strategy"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar first!")
    elif not uploaded_file:
        st.error("Please upload your Date Sheet image.")
    elif not syllabus_text:
        st.error("Please enter your syllabus.")
    else:
        # Show a loading spinner while AI thinks
        with st.spinner("Analyzing your exam dates..."):
            try:
                # Configure the AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                # Load the image
                image = Image.open(uploaded_file)

                # The Prompt (Instructions for the AI)
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
                
                # Display the result
                st.success("Plan Generated!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
