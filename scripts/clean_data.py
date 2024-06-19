import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# function to clean text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    # remove URLs
    text = re.sub(r'http\S+', '', text)
    # convert to lowercase
    text = text.lower()
    # remove punctuation and special characters
    text = re.sub(r'\W', ' ', text)
    # remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    # lemmatize words
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # join tokens back to a single string
    cleaned_text = ' '.join(tokens)
    return cleaned_text

# load dataset with specified encoding
df = pd.read_csv('train.csv', encoding='ISO-8859-1')

# fill missing values in 'text' column with empty strings
df['text'] = df['text'].fillna("")

# apply the clean_text function to each post
df['clean_text'] = df['text'].apply(clean_text)

# display the first few rows of the cleaned dataframe
print(df[['text', 'clean_text']].head())

# save the cleaned DataFrame to a new CSV file 
df.to_csv('cleaned_train.csv', index=False)
