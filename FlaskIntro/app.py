# Import Flask and required functions
from flask import Flask, request, render_template
from helper_functions import preprocess_text, interpret_prediction

app = Flask(__name__)

# Import model 
import pickle
import pytesseract
import cv2
import numpy as np
import base64

# Load model
with open('model_0_baseline.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    # if user submits an image, use pytesseract to extract text and make a prediction
    if request.method == 'POST': 
        image = request.files['file']
        img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        text = pytesseract.image_to_string(img)
        processed_text = preprocess_text(text)
        prediction = model.predict_proba(processed_text)
        prediction = interpret_prediction(prediction)
        classes = model.classes_
        predicted_class = model.predict(processed_text)
        _, encoded_img = cv2.imencode('.jpg', img)  # Encode as JPEG
        image_data = base64.b64encode(encoded_img).decode('utf-8')

        return render_template('index.html', prediction=prediction, classes=classes, text=text, predicted_class=predicted_class, image_data=image_data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)