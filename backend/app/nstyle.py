from flask import Flask, jsonify, request
import sys
import os
import tempfile
from werkzeug import secure_filename
from flask import send_file
from flask_cors import CORS
import io
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove
import cv2
import numpy as np
from PIL import Image
from app.nstylemodel.helper import load_img, preprocess_content_image, preprocess_style_image, run_style_predict, run_style_transform
print("=============================== neural model loaded")

# creating the Flask application
app = Flask(__name__)
CORS(app)


@app.route('/nstylehome', methods = ['POST','GET'])
def nstylehome():
    # pretending load models
    return jsonify("at neuralstyle home.")

@app.route("/mash", methods=['POST'])
def mash():
    # preprocessing images 
    style_img = request.files['style_img']
    cntnt_img = request.files['cntnt_img']
    style_img = Image.open(style_img)
    cntnt_img = Image.open(cntnt_img)
    print(type(style_img))
    print(type(cntnt_img))
    style_img = np.asarray(style_img, dtype=np.uint8)
    cntnt_img = np.asarray(cntnt_img, dtype=np.uint8)
    print("=============================== image files arrived from request")
    style_img = load_img(style_img)
    cntnt_img = load_img(cntnt_img)
    preprocessed_content_image = preprocess_content_image(style_img)
    preprocessed_style_image = preprocess_style_image(cntnt_img)
    print('Style Image Shape:', preprocessed_style_image.shape)
    print('Content Image Shape:', preprocessed_content_image.shape)
    print("=============================== image preprocessed")
    style_bottleneck = run_style_predict(preprocessed_style_image)
    print('Style Bottleneck Shape:', style_bottleneck.shape)
    stylized_image = run_style_transform(style_bottleneck, preprocessed_content_image)
    print("=============================== model initialized")
    image = stylized_image.squeeze(0)      # remove the fake batch dimension
    
    print("=============================== neural model ran")

    imgio = io.BytesIO()
    image.save(imgio, 'JPEG')
    imgio.seek(0)
    return send_file(imgio, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host="0.0.0.0")