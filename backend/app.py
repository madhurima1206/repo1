from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import re
import os

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(
    __name__,
    static_folder='static/build',
    static_url_path=''
)

CORS(app)

# Load ML model
model = pickle.load(open('models/model.pkl', 'rb'))

# Load vectorizer
vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))

ps = PorterStemmer()

# Text preprocessing
def transform_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    words = text.split()

    words = [word for word in words if word not in stopwords.words('english')]

    words = [ps.stem(word) for word in words]

    return " ".join(words)

# Prediction API
@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    message = data['message']

    processed_message = transform_text(message)

    vector_input = vectorizer.transform([processed_message])

    result = model.predict(vector_input)[0]

    if result == 1:
        prediction = "Spam Email 🚨"
    else:
        prediction = "Not Spam ✅"

    return jsonify({
        "prediction": prediction
    })

# Serve React frontend
@app.route('/')
def serve():

    return send_from_directory(app.static_folder, 'index.html')

# Run app
if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)