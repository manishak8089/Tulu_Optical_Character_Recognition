import streamlit as st
import cv2
import joblib
import os
import numpy as np
from skimage import io, color, transform
import requests
from io import BytesIO

# Function to load the model from a URL
def load_model_from_url(url):
    response = requests.get(url)
    model_file = BytesIO(response.content)
    return joblib.load(model_file)

# Load your trained model from GitHub release
model_url = 'https://github.com/manishak8089/Tulu_Optical_Character_Recognition/releases/download/v1.0/random_forest_model.pkl'
model = load_model_from_url(model_url)

# Function to read and preprocess images along with labels
def load_and_preprocess_images(folder_path):
    images = []
    labels = []

    for label in os.listdir(folder_path):
        label_path = os.path.join(folder_path, label)

        for filename in os.listdir(label_path):
            img_path = os.path.join(label_path, filename)
            img = io.imread(img_path)

            # Preprocess the image (you may need to adjust this based on your images)
            img = transform.resize(color.rgb2gray(img), (64, 64))

            images.append({
                'image': img.flatten(),  # Flatten the image into a 1D array
                'label': label,
                'filename': filename  # Store the filename for reference
            })

    return images

# Streamlit UI
st.title("Tulu OCR Application")

# Image upload widget
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Preprocess the uploaded image
    uploaded_image = io.imread(uploaded_file)

    # Check if the image has an alpha channel (transparency)
    if uploaded_image.shape[-1] == 4:
        # If alpha channel exists, remove it
        uploaded_image = uploaded_image[:, :, :3]

    # Resize and convert to grayscale
    processed_image = transform.resize(color.rgb2gray(uploaded_image), (64, 64))
    flattened_image = processed_image.flatten()

    # Make predictions
    prediction = model.predict(flattened_image.reshape(1, -1))

    # Display the original image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Display the OCR result along with label and filename
    st.write("OCR Result: ")
    st.write(f"The image found in the folder named: {prediction[0]}")

# Display images with labels and filenames from the dataset
folder_path = 'C:\\Users\\manis\\Tulu lipi codes\\aug_resized_images2'  # Update with the actual path to your dataset
#dataset_images = load_and_preprocess_images(folder_path)

#for data in dataset_images:
 #   st.image(data['image'].reshape((64, 64)), caption=f"Label: {data['label']}, Filename: {data['filename']}", use_column_width=True)
