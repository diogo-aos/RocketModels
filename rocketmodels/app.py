from __future__ import print_function
import os
import tempfile
import argparse

from flask import Flask, request, redirect, url_for
from flask import jsonify
from werkzeug.utils import secure_filename

from model import run_all_models

input_height = 299
input_width = 299
input_mean = 0
input_std = 255
input_layer = "Placeholder"
output_layer = "final_result"
PORT = 5000

parser = argparse.ArgumentParser()
parser.add_argument("--input_height", type=int, help="input height", default=input_height)
parser.add_argument("--input_width", type=int, help="input width", default=input_width)
parser.add_argument("--input_mean", type=int, help="input mean", default=input_mean)
parser.add_argument("--input_std", type=int, help="input std", default=input_std)
parser.add_argument("--input_layer", help="name of input layer", default=input_layer)
parser.add_argument("--output_layer", help="name of output layer", default=output_layer)
parser.add_argument("--port", help="port to use", default=PORT)
args = parser.parse_args()


#UPLOAD_IMAGE_FN = tempfile.mkstemp()

UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return 'working...', 200
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file in request')
            return 'no file in request'

        file = request.files['file']

        # empty filename error
        if file.filename == '':
            print('empty filename')
            return 'empty filename', 400

        # file without extension error
        if '.' not in file.filename:
            return 'file without extension', 400

        file_extension = file.filename.rsplit('.', 1)[1].lower()

        # bad extension error
        if file_extension not in ALLOWED_EXTENSIONS:
            return 'extension {} not allowed; allowed extensions are {}'.format(file_extension, ALLOWED_EXTENSIONS), 400

        if file:
            filename = 'image.{}'.format(file_extension)
            fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fn)
            print('received file saved in {}'.format(fn))
            print('running all models...')
            results = run_all_models(fn, args)

            return jsonify(results)
            
    return 'not ok',200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
