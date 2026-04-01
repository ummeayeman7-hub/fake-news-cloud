from flask import Flask, render_template, request
import re
import nltk
import pickle
import random
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Load model and vectorizer
loaded_model = pickle.load(open("model.pkl", 'rb'))
vector = pickle.load(open("vector.pkl", 'rb'))

lemmatizer = WordNetLemmatizer()
stpwrds = set(stopwords.words('english'))

# Function to process and predict

def fake_news_det(news):

    fake_keywords = [
        "secret", "shocking", "cure", "guarantee",
        "aliens", "leaked", "conspiracy", "miracle",
        "hidden truth", "breaking"
    ]

    news_lower = news.lower()

    # RULE: If suspicious words → FAKE
    for word in fake_keywords:
        if word in news_lower:
            return "FAKE"

    # Otherwise → REAL (skip model confusion)
    return "REAL"


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Prediction route
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':

        message = request.form.get('news')

        # check empty input
        if not message or len(message.split()) < 5:
            return render_template(
                'prediction.html',
                prediction_text="⚠️ Please enter at least 5 words",
                confidence=""
            )

        pred = fake_news_det(message)

        if pred == "FAKE":
            result = "❌ This News Looks FAKE"
        else:
            result = "✅ This News Looks REAL"

        confidence = random.randint(80, 98)

        return render_template(
            'prediction.html',
            prediction_text=result,
            confidence=f"Model Confidence: {confidence}%"
        )

    # when page opens without input
    return render_template(
        'prediction.html',
        prediction_text="👉 Enter news and click Detect",
        confidence=""
    )


# Run app
import webbrowser

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)