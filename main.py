import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np

# Load the model
model = tf.keras.models.load_model('gamify.h5')

# Define the list of game labels
game_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Define the Streamlit app
def main():
    st.title('Game Predictor')
    st.write('Upload an image and the model will predict the corresponding game.')

    # Display file uploader to upload the image
    uploaded_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Read the image file
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Preprocess the image
        image = preprocess_image(image)

        # Make prediction
        prediction = make_prediction(image)

        # Display the predicted game
        st.write('Prediction:', game_labels[prediction])

# Preprocess the image
def preprocess_image(image):
    # Convert the image to RGB mode
    image = image.convert('RGB')
    # Resize the image to the required input shape of the model
    image = image.resize((224, 224))
    # Convert the image to an array
    image = np.array(image)
    # Normalize the image
    image = image / 255.0
    # Expand the dimensions to match the model's input shape
    image = np.expand_dims(image, axis=0)
    return image

# Make prediction
def make_prediction(image):
    # Make prediction using the loaded model
    prediction = model.predict(image)
    # Get the predicted game label
    predicted_label = np.argmax(prediction)
    return predicted_label

# Run the app
if __name__ == '__main__':
    main()
