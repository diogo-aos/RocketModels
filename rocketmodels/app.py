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
input_layer = "input"
output_layer = "InceptionV3/Predictions/Reshape_1"
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


UPLOAD_IMAGE_FN = tempfile.mkstemp()

UPLOAD_FOLDER = '/tmp/'
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
            return 'file type not supported, allowed extensions:{}'.format(ALLOWED_EXTENSIONS)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'empty filename'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fn)

            results = run_all_models(fn, args)

            return jsonify(results)
            
    return 'not ok',200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port, debug=True)
