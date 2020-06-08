import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    import gad1
    image = request.form['image']
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