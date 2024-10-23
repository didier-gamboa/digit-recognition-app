import os
import requests
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


URL_BACKEND = os.getenv("URL_BACKEND", "http://localhost:8000/predict")

def classify_digit(img):
    response = requests.post(URL_BACKEND, json={"image": img.tolist()})
    response = response.json()
    return response['predicted_label'], response['predicted_proba']

st.set_page_config(page_title="Digit Recognition", page_icon="✏️")
st.title("🖍️ Handwritten Digit Recognition")
st.markdown("Draw a digit between **0 and 9** on the canvas and classify it.")

# Expander with additional information
with st.expander("ℹ️ Instructions"):
    st.write("""
    1. Draw a digit between **0 and 9** on the canvas on the left.
    2. Click **Classify!** to see the result.
    3. The image will be automatically resized to 28x28 pixels.
    4. Check the predicted digit and the probabilities for each class.
    """)
    
col1, col2 = st.columns(2)

# Canvas for drawing (250x250 px)
with col1:
    st.subheader("📝 Draw Your Digit")
    canvas = st_canvas(
        width=250, height=250, drawing_mode="freedraw", 
        stroke_width=10, stroke_color="#000000"
    )

# Button to classify the digit
if st.button("Classify!") and canvas.image_data is not None:
    # Convert canvas image to grayscale and resize to 28x28
    img = canvas.image_data[:, :, 3]  # Alpha channel (transparency)
    img = Image.fromarray(img).resize((28, 28), Image.LANCZOS)
    img_array = np.array(img)

    # Display the resized image in the right column
    with col2:
        st.subheader("📏 Resized Image (28x28)")
        st.image(img_array, width=150, clamp=True, caption="Grayscale Image")

    # Classify the digit and display the result
    label, prob = classify_digit(img_array)
    st.metric("Prediction", f"{label}")

    # Create a bar chart with the probabilities
    fig, ax = plt.subplots()
    ax.bar(range(10), prob[0], color='skyblue')
    ax.set_xlabel("Digit")
    ax.set_ylabel("Probability")
    ax.set_title("Class Probabilities")
    ax.set_xticks(range(10))

    # Display the bar chart in Streamlit
    st.pyplot(fig)

