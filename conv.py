import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the saved .h5 model
loaded_model = load_model('gamify.h5')

# Save the model in TensorFlow format
tf.saved_model.save(loaded_model, 'gamify')
