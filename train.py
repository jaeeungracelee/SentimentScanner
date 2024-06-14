import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

df = pd.read_csv('datasets/test.csv', encoding='latin-1')

print(df.head())

def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

df['text'] = df['text'].fillna('')

df['text'] = df['text'].apply(preprocess_text)

# vectorize using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['text']).toarray()

df['sentiment'] = df['sentiment'].map({'negative': 0, 'neutral': 2, 'positive': 4})
df = df.dropna(subset=['sentiment'])

# align X and Y with non-NaN values
X = vectorizer.transform(df['text']).toarray()
y = df['sentiment'].values

# check if theres any NaN in X
X = np.nan_to_num(X)

# split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))