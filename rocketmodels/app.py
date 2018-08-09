import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

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
        return 'working...'
    if request.method == 'POST':
        print(request.files)
        print(dir(request.files))
        print('hello0')
        print(request.files.get('file'))
        print('hello')
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
            print(dir(file))
            print(fn)
            file.save(fn)
            return 'file saved in {}'.format(fn), 200
    return 'ok',200
