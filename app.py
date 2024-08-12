from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF
import base64
import google.generativeai as genai
import io

# Load environment variables
load_dotenv()

# Check if the Google API key is available
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found. Please set it in the .env file.")
    st.stop()

# Configure Google Generative AI with the API key
genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    
    full_prompt = f"{prompt}\n\nJob Description:\n{input_text}\n\nResume Content:\n{pdf_content}"
    
    response = model.generate_content(full_prompt)
    
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = doc.load_page(0)
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes("jpeg")
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        text = first_page.get_text("text")
        return text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit page configuration
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f0f5;
        color: #333;
        font-family: Arial, sans-serif;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .header {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with custom styling
st.markdown('<div class="header"><h1>ATS Tracking System</h1></div>', unsafe_allow_html=True)

# Input text area for job description
input_text = st.text_area("Job Description:", key="input", height=150)

# File uploader for the resume PDF
uploaded_file = st.file_uploader("Upload your resume (PDF only)...", type=["pdf"])

# Prompts for the AI
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. 
Give me the percentage match if the resume matches the job description. First, the output should come as a percentage, then keywords missing, and lastly, final thoughts.
"""

# Buttons for different actions
col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("Tell Me About the Resume")
with col2:
    submit3 = st.button("Percentage Match")

# Action for the first button
if submit1 and uploaded_file is not None:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
elif submit1:
    st.warning("Please upload the resume")

# Action for the third button
if submit3 and uploaded_file is not None:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
elif submit3:
    st.warning("Please upload the resume")
