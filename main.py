###
# Matting code
import os
from flask_assets import Bundle, Environment
from werkzeug.utils import secure_filename
from flask import request, flash, redirect, url_for
from flask import render_template
from flask import Flask
import time
# import imutils
from PIL import Image
import numpy as np
import math
import cv2
from copy import deepcopy

app = Flask(__name__)

uploads_dir = "static/uploads/"
app_uploads_dir = "static/app-uploads/"
os.makedirs(uploads_dir, exist_ok=True)

# set up for multiple js files, only need to add to this bundle in the future
js = Bundle('main.js', output='gen/output.js')
assets = Environment(app)
assets.register('main_js', js)

# Filtering allowed files
ALLOWED_EXTENSIONS = set(['jpg, png'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        print(request.files)

        image_num = 8

        for i in range(1, image_num+1):
            if 'image' + str(i) not in request.files:
                flash('No uploaded images')
                render_template('index.html',
                                init_hidden_class="hidden",
                                later_hidden_class="")
            rgb_img = request.files.get('image' + str(i))
            if rgb_img.filename == '':
                flash('No uploaded video')
                render_template('index.html',
                                init_hidden_class="hidden",
                                later_hidden_class="")
            if rgb_img and allowed_file(rgb_img.filename):
                os.system('rm -rf static/uploads/image' + str(i) + '.png')
                rgb_img.save(os.path.join(uploads_dir, 'image' + str(i) + '.png'))
                while not os.path.exists('static/uploads/' + 'image' + str(i) + '.png'):
                    pass
        os.system('sh runRecon.sh')
        
    return render_template('index.html',
                           init_hidden_class="hidden",
                           later_hidden_class="",
                           foreground='static/uploads/result.mp4')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8010, debug=True)
