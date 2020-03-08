import tensorflow.compat.v2 as tf
import numpy as np
import time
import functools
tf.enable_v2_behavior()

style_predict_path = tf.keras.utils.get_file('style_predict.tflite', 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/arbitrary_style_transfer/style_predict_quantized_256.tflite')
style_transform_path = tf.keras.utils.get_file('style_transform.tflite', 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/arbitrary_style_transfer/style_transfer_quantized_dynamic.tflite')

# Function to load an image from a file, and add a batch dimension.
def load_img(data):
    # img = tf.io.read_file(path_to_img)
    # img = tf.image.decode_image(path_to_img, channels=3)
    img = tf.image.convert_image_dtype(data, tf.float32)
    img = img[tf.newaxis, :]
    print(img.shape)
    return img

# Function to pre-process style image input.
def preprocess_style_image(style_image):
    # Resize the image so that the shorter dimension becomes 256px.
    target_dim = 256
    shape = tf.cast(tf.shape(style_image)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = target_dim / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    style_image = tf.image.resize(style_image, new_shape)

    # Central crop the image.
    style_image = tf.image.resize_with_crop_or_pad(style_image, target_dim, target_dim)

    return style_image

# Function to pre-process content image input.
def preprocess_content_image(content_image):
    # Central crop the image.
    shape = tf.shape(content_image)[1:-1]
    short_dim = min(shape)
    content_image = tf.image.resize_with_crop_or_pad(content_image, short_dim, short_dim)

    return content_image

# Function to run style prediction on preprocessed style image.
def run_style_predict(preprocessed_style_image):
    # Load the model.
    interpreter = tf.lite.Interpreter(model_path=style_predict_path)

    # Set model input.
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)

    # Calculate style bottleneck.
    interpreter.invoke()
    style_bottleneck = interpreter.tensor(
      interpreter.get_output_details()[0]["index"]
      )()

    return style_bottleneck
# Run style transform on preprocessed style image
def run_style_transform(style_bottleneck, preprocessed_content_image):
    print(".......transforming")
    # Load the model.
    interpreter = tf.lite.Interpreter(model_path=style_transform_path)
    print(".......set model input")
    # Set model input.
    input_details = interpreter.get_input_details()
    interpreter.resize_tensor_input(input_details[0]["index"],
                                  preprocessed_content_image.shape)
    interpreter.allocate_tensors()
    print(".......invoking ...")
    # Set model inputs.
    interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()
    print(".......transforming content image ...")
    # Transform content image.
    stylized_image = interpreter.tensor(
      interpreter.get_output_details()[0]["index"]
      )()

    return stylized_image