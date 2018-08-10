import os
import tempfile

from flask import Flask, request, redirect, url_for
from flask import jsonify
from werkzeug.utils import secure_filename



from .models import run_all_models



UPLOAD_IMAGE_FN = tempfile.mkstemp()
UPLOAD_FOLDER = '/home/diogoaos/workspace/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
            file.save(UPLOAD_IMAGE_FN)

            results = run_all_models(UPLOAD_IMAGE_FN)

            return jsonify(results)
            
    return 'not ok',200
