from flask import Flask, request, jsonify
from flask_cors import CORS
import tweepy
import praw
import re
import os
from dotenv import load_dotenv, find_dotenv
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

app = Flask(__name__)
CORS(app)

# load environment variables from .env file in the root directory
env_path = find_dotenv()
load_dotenv(dotenv_path=env_path)

# twitter API credentials
# twitter_api_key = os.getenv('TWITTER_API_KEY')
# twitter_api_secret = os.getenv('TWITTER_API_SECRET')
# twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
# twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')

# reddit API credentials
reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

# set up Twitter API
# auth = tweepy.OAuth1UserHandler(twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret)
# twitter_api = tweepy.API(auth)

# set up Reddit API
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

# disable SSL verification for NLTK downloads 
# please work... 
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# initialize NLTK tools and ensure all necessary resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# remove stop words
stop_words = set(stopwords.words('english'))
sid = SentimentIntensityAnalyzer()

def preprocess_text(text):
    # remove URLs
    text = re.sub(r'http\S+', '', text)
    # change to lowercase
    text = text.lower()
    # remove punctuation and special characters
    text = re.sub(r'\W', ' ', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    # lemmatize words
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# def fetch_tweets(keyword):
#     tweets = twitter_api.search_tweets(q=keyword, count=100, lang='en', tweet_mode='extended')
#     return [tweet.full_text for tweet in tweets]

def fetch_reddit_posts(keyword):
    posts = reddit.subreddit('all').search(keyword, limit=100)
    return [post.title + ' ' + post.selftext for post in posts]

def analyze_sentiment(texts):
    return [sid.polarity_scores(preprocess_text(text)) for text in texts]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    keyword = data['keyword']
    # tweets = fetch_tweets(keyword)
    reddit_posts = fetch_reddit_posts(keyword)
    # tweet_sentiments = analyze_sentiment(tweets)
    reddit_post_sentiments = analyze_sentiment(reddit_posts)

    # tweet_df = pd.DataFrame(tweet_sentiments)
    reddit_df = pd.DataFrame(reddit_post_sentiments)

    return jsonify({
        # 'tweet_df': tweet_df.to_html(),
        'reddit_df': reddit_df.to_html()
    })

if __name__ == '__main__':
    app.run(debug=True)
