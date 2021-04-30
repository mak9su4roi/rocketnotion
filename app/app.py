from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response
import base64
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename
from utils import utils

import os

IMAGE_UPLOADS = '.tmp/'
IMAGE_EXTENSIONS = {'jpeg', 'jpg', 'png'}


app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = IMAGE_UPLOADS
app.config["ALLOWED_IMAGE_EXTENSIONS"] = IMAGE_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html', content='<h3>Hi there! 📽</h3>')


@app.route('/upload', methods=['POST'])
def gen_image():
    if request.files:
        file = request.files["image"]
        file_name = file.filename

    else:
        if not request.data:
            return render_template('main.html', content='<h3>Hi there! 📽</h3>')

        file_name = request.args['image_name'].lower()
        file = str(request.data)

        image_data = bytes(file[file.find(',')+1:], encoding="ascii")
        file = Image.open(BytesIO(base64.b64decode(image_data)))

    if not file_name:
        return redirect('/')

    if not utils.allowed_image(file_name, IMAGE_EXTENSIONS):
        return redirect('/')

    file.save(os.path.join(app.config['IMAGE_UPLOADS'], file_name))
    print('[UPDATE]: NEW FILE SAVED: ', file_name)

    return render_template('main.html', content='<h3>Hi there! 📽</h3>')


@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template("result.html", content='<h3>Should be something here 📽</h3>')


if __name__ == "__main__":
    app.run(host='localhost', port=8001, debug=True)
