from flask import Flask, jsonify, request
import sys
import os
from werkzeug import secure_filename
from flask import send_file
from flask_cors import CORS
from app.nstylemodel.helper import image_loader,\
                                models,\
                                torch,\
                                run_style_transfer,\
                                device,\
                                transforms

# creating the Flask application
app = Flask(__name__)
CORS(app)
NEURAL_MODEL = None
STYLE_IMG = None
CONTENT_IMG = None
CNN_NORMALIZATION_MEAN = None
CNN_NORMALIZATION_STD = None
CONTENT_LAYERS_DEFAULT = None
STYLE_LAYERS_DEFAULT = None
PROGRESS = None
ITRS = 0

@app.route('/nstylehome', methods = ['POST','GET'])
def nstylehome():
    global NEURAL_MODEL
    NEURAL_MODEL = models.vgg19(pretrained=True).features.to(device).eval()            
    # pretending load models
    print(NEURAL_MODEL,sys.stderr)
    return jsonify("model loaded.")

@app.route('/upload_style', methods=['POST'])
def nstyle_upload_style():
    print("style reached backend server upload")
    print(request,sys.stderr)
    f = request.files['image']
    f.save("style_img.jpg")
    print("style image uploaded to server",sys.stderr)
    return jsonify("image uploaded to server")

@app.route('/upload_content', methods=['POST'])
def nstyle_upload_content():
    print("content reached backend server upload")
    print(request,sys.stderr)
    f = request.files['image']
    f.save("content_img.jpg")
    print("content image uploaded to server",sys.stderr)
    return jsonify("image uploaded to server")

@app.route('/load_images',methods=['GET'])
def load_images():
    global STYLE_IMG
    global CONTENT_IMG
    STYLE_IMG = image_loader("style_img.jpg",h=True)
    CONTENT_IMG = image_loader("content_img.jpg",h=True)
    return jsonify("Images are loaded")

@app.route('/initialize_model',methods=['GET'])
def initialize_model():
    global CNN_NORMALIZATION_MEAN
    global CNN_NORMALIZATION_STD
    global CONTENT_LAYERS_DEFAULT
    global STYLE_LAYERS_DEFAULT
    global ITRS
    CONTENT_LAYERS_DEFAULT = ['conv_4']
    STYLE_LAYERS_DEFAULT = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
    CNN_NORMALIZATION_MEAN = torch.tensor([0.485, 0.456, 0.406]).to(device)
    CNN_NORMALIZATION_STD = torch.tensor([0.229, 0.224, 0.225]).to(device)
    
    return jsonify("Neural model initialized")

@app.route('/optimize',methods=['GET'])
def optimize():
    global ITRS
    if ITRS == 0:
        INPUT_IMG = CONTENT_IMG.clone()
    else:
        INPUT_IMG = image_loader("output.jpg", h=True)
    ITRS += 1
    PROGRESS = run_style_transfer(NEURAL_MODEL,\
                                CNN_NORMALIZATION_MEAN,\
                                CNN_NORMALIZATION_STD,\
                                CONTENT_IMG,\
                                STYLE_IMG,\
                                INPUT_IMG,\
                                CONTENT_LAYERS_DEFAULT,\
                                STYLE_LAYERS_DEFAULT,
                                num_steps=15)
    unloader = transforms.ToPILImage()  # reconvert into PIL image
    print("!!!!!!!!!",sys.stderr)
    image = PROGRESS.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)      # remove the fake batch dimension
    image = unloader(image)
    image.save("output.jpg")
    return send_file("../output.jpg", mimetype='image/*')

@app.route('/dnload', methods=['GET'])
def nstyle_dnload():
    # delete output.img if it exists:
    if os.path.exists("output.jpg"):
        os.remove("output.jpg")
    print("!!!!!!!!!",sys.stderr)
    style_img = image_loader("style_img.jpg",h=True)
    content_img = image_loader("content_img.jpg",h=True)
    print(style_img.shape,sys.stderr)
    print(content_img.shape,sys.stderr)

    cnn = NEURAL_MODEL
    cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
    cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)
    input_img = content_img.clone()
    print("!!!!!!!!!",sys.stderr)

    content_layers_default = ['conv_4']
    style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
    output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                                content_img, style_img, input_img,\
                                content_layers_default,style_layers_default)
    unloader = transforms.ToPILImage()  # reconvert into PIL image
    print("!!!!!!!!!",sys.stderr)
    image = output.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)      # remove the fake batch dimension
    image = unloader(image)
    image.save("output.jpg")
    print("reached backend server",sys.stderr)
    return send_file("../output.jpg", mimetype='image/*')

if __name__ == '__main__':
    app.run(host="0.0.0.0")