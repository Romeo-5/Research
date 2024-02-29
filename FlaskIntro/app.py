# Import Flask and required functions
from flask import Flask, request, render_template
from helper_functions import preprocess_text, interpret_prediction

app = Flask(__name__)

# Import model 
import pickle
import pytesseract
import cv2
import numpy as np

# Load model
with open('model_0_baseline.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    # if user submits an image, use pytesseract to extract text
    """"
    if request.method == 'POST':
        image = request.files['file']
        img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        text = pytesseract.image_to_string(img)
        processed_text = preprocess_text(text)
        prediction = model.predict_proba(processed_text)
        prediction = interpret_prediction(prediction)
        classes = model.classes_
        predicted_class = model.predict(processed_text)
    """
    
    if request.method == 'POST':
        text = request.form['user_input']  # Get text from form
        processed_text = preprocess_text(text)  # Apply your preprocessing
        prediction = model.predict_proba(processed_text)  # Get prediction probabilities
        prediction = interpret_prediction(prediction) # Translate to string 
        classes = model.classes_ # Get classes
        predicted_class = model.predict(processed_text) # Get predicted class

        return render_template('index.html', prediction=prediction, classes=classes, text=text, predicted_class=predicted_class)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)