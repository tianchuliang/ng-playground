from flask import Flask, jsonify, request
import sys
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

@app.route('/dnload', methods=['GET'])
def nstyle_dnload():
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