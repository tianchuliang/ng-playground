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


class nystyle_obj():
    def __init__(self):
        self.NEURAL_MODEL = None
        self.STYLE_IMG = None
        self.CONTENT_IMG = None
        self.CNN_NORMALIZATION_MEAN = None
        self.CNN_NORMALIZATION_STD = None
        self.CONTENT_LAYERS_DEFAULT = None
        self.STYLE_LAYERS_DEFAULT = None
        self.PROGRESS = None
        self.ITRS = 0

    def set_images(self, CONTENT_IMG, STYLE_IMG):
        self.CONTENT_IMG = CONTENT_IMG
        self.STYLE_IMG = STYLE_IMG
    
    def init_model(self):
        self.CONTENT_LAYERS_DEFAULT = ['conv_4']
        self.STYLE_LAYERS_DEFAULT = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
        self.CNN_NORMALIZATION_MEAN = torch.tensor([0.485, 0.456, 0.406]).to(device)
        self.CNN_NORMALIZATION_STD = torch.tensor([0.229, 0.224, 0.225]).to(device)
    
    def optimize(self):
        if self.ITRS == 0:
            self.INPUT_IMG = self.CONTENT_IMG.cpu.clone()
        else:
            self.INPUT_IMG = self.PROGRESS
        self.ITRS += 1
        self.PROGRESS = run_style_transfer(self.NEURAL_MODEL,\
                                            self.CNN_NORMALIZATION_MEAN,\
                                            self.CNN_NORMALIZATION_STD,\
                                            self.CONTENT_IMG,\
                                            self.STYLE_IMG,\
                                            self.INPUT_IMG,\
                                            self.CONTENT_LAYERS_DEFAULT,\
                                            self.STYLE_LAYERS_DEFAULT,
                                            num_steps=5)
        return self.PROGRESS


@app.route('/nstylehome', methods = ['POST','GET'])
def nstylehome():
    # pretending load models
    return jsonify("at neuralstyle home.")

@app.route("/mash", methods=['POST'])
def mash():
    NEURAL_MODEL = models.vgg19(pretrained=True).features.to(device).eval()
    styleobj = nystyle_obj()
    styleobj.NEURAL_MODEL = NEURAL_MODEL
    # preprocessing images 
    
    style_img = request.files['style_img']
    cntnt_img = request.files['content_img']

    # the folloing maynot work
    style_img = image_loader(style_img,h=True)
    cntnt_img = image_loader(cntnt_img,h=True)
    styleobj.set_images(cntnt_img, style_img)
    styleobj.init_model()
    result = styleobj.optimize()

    pass


# @app.route('/initialize_model',methods=['GET'])
# def initialize_model():
#     session['model'].init_model() 
#     return jsonify("Neural model initialized")

# @app.route('/optimize',methods=['GET'])
# def optimize():
#     unloader = transforms.ToPILImage()  # reconvert into PIL image
#     print("!!!!!!!!!",sys.stderr)
#     PROGRESS = session['model'].optimize()
#     image = PROGRESS.cpu().clone()  # we clone the tensor to not do changes on it
#     image = image.squeeze(0)      # remove the fake batch dimension
#     image = unloader(image)
#     image.save("output.jpg")
#     return send_file("../output.jpg", mimetype='image/*')

if __name__ == '__main__':
    app.run(host="0.0.0.0")