import numpy as np
from flask import Flask, request, jsonify, render_template, flash
import os
import pickle
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'faces/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
    else:
        return render_template('index.html')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    upload_file()
    import gad1
    image = request.files['file']
    image = image.filename
    if gad1.show(image):
        return render_template('predict.html', image=image)
    else:
        return render_template('index.html')


@app.route('/capture',methods=['POST', 'GET'])
def capture():
    '''
    For rendering results on HTML GUI
    '''
    import gad1
    filename = gad1.capture()
    import time
    time.sleep(2)
    return render_template('predict.html', image=filename)





@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)