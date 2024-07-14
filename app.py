import streamlit as st
from transformers import pipeline
import os
import base64
# Load a pre-trained model for text generation
generator = pipeline('text-generation', model='gpt2')

def generate_recommendation(user_input):
    prompt = f"Given the following user input, provide a career recommendation:\n\nUser Input: {user_input}\n\nCareer Recommendation:"
    recommendations = generator(prompt, max_length=1000, num_return_sequences=1,truncation=True, pad_token_id=50256)
    return recommendations[0]['generated_text']

def set_background_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"Background image file not found: {image_path}")

# Set the background image
set_background_image('images/background.jpg')  # Ensure this path is correct

st.title("CareerVision")
st.markdown("<h2 style='text-align: center;'>Welcome to CareerVision! Get personalized career recommendations.</h2>", unsafe_allow_html=True)

st.write("Please fill in the following details to get your career recommendation:")


# User inputs
skills = st.text_area("Skills (e.g., programming, writing, data analysis):")
interests = st.text_area("Interests (e.g., technology, arts, sports):")
academic_background = st.text_area("Academic Background (e.g., degree, major, courses):")
work_experience = st.text_area("Work Experience (if any):")
other_info = st.text_area("Other Information (e.g., hobbies, projects, career goals):")

user_input = f"Skills: {skills}\nInterests: {interests}\nAcademic Background: {academic_background}\nWork Experience: {work_experience}\nOther Information: {other_info}"

if st.button("Get Career Recommendation"):
    with st.spinner("Generating recommendation..."):
        recommendation = generate_recommendation(user_input)
        st.success("Here is your career recommendation:")
        st.write(recommendation)
