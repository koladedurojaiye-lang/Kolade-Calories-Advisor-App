import os

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Missing GOOGLE_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=api_key)


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("models/gemini-3.8-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    bytes_data = uploaded_file.getvalue()
    image_parts = [
        {
            "mime_type": uploaded_file.type,
            "data": bytes_data,
        }
    ]
    return image_parts


st.set_page_config(page_title="Kolade Calories Advisor App")
st.header("Kolade Calories Advisor App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
submit = False
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    submit = st.button("Get Calories Information")

input_prompt = """
You are an expert nutritionist. Look at the image and calculate the total calories. Provide details of each food item with calories in this format:

1. Item 1: No. of calories
2. Item 2: No. of calories

Finally, mention whether the food is healthy or not and include the percentage split of carbohydrates, fats, fiber, protein, sugar, and other important dietary components.
"""

if submit:
    if uploaded_file is None:
        st.warning("Please upload an image first.")
    else:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("The Response is")
        st.write(response)