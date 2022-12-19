from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file in files:
            path = os.path.dirname(file.filename)
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], path)
            if not os.path.exists(path2):
                os.mkdir(path2)
            filename = os.path.join(path, secure_filename(
                os.path.basename(file.filename)))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Files uploaded.'
    return render_template('upload2.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4040)
