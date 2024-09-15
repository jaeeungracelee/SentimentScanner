from flask import Flask, request, jsonify
from flask_cors import CORS
import tweepy
import praw
import re
import os
from dotenv import load_dotenv, find_dotenv
import nltk
import ssl
import pickle
import joblib
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

app = Flask(__name__)
CORS(app)

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words('english'))
sid = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return "Welcome to the Sentiment Scanner!"

def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    keyword = data['keyword']
    
    try:
        print(f"Received keyword: {keyword}")
        
        # Check if vectorizer file exists
        if not os.path.exists('count_vectorizer.pkl'):
            raise FileNotFoundError('count_vectorizer.pkl not found')
        
        # Check if model file exists
        if not os.path.exists('random_forest_model_69_acc.pkl'):
            raise FileNotFoundError('random_forest_model_69_acc.pkl not found')
        
        print("Loading vectorizer...")
        with open('count_vectorizer.pkl', 'rb') as file:
            loaded_vectorizer = pickle.load(file)

        vec_keyword = loaded_vectorizer.transform([keyword])
        vec_keyword = vec_keyword.toarray()

        print("Loading model...")
        joblib_file = "random_forest_model_69_acc.pkl"
        loaded_model = joblib.load(joblib_file)

        print("Making predictions...")
        predictions = loaded_model.predict(vec_keyword)
        print(f"Predictions: {predictions}")

        return jsonify({
            'reddit_df': predictions[0]
        })
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
        return jsonify({'error': f"File not found: {str(e)}"}), 500
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)