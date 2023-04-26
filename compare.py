from flask import Flask, jsonify
from pymongo import MongoClient
import json
import glob
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.pdfs
collection = db.text_files

# Tokenize, remove stop words and punctuation, and preprocess the documents
docs = []
stopwords = nltk.corpus.stopwords.words("english")
for file in collection.find():
    tokens = word_tokenize(file['text'].lower())
    filtered = [word for word in tokens if word not in stopwords and word.isalpha()]
    preprocessed = " ".join(filtered)
    docs.append(preprocessed)

# Vectorize the documents
vectorizer = TfidfVectorizer()
vectorizer.fit(docs)
docs_vectorized = vectorizer.transform(docs)

@app.route('/files/<text>')
def get_all_files(text):
    similarity_scores = cosine_similarity(vectorizer.transform([text]), docs_vectorized)
    most_similar_index = similarity_scores.argmax()
    similarity_score = similarity_scores[0][most_similar_index]
    
    most_similar_index = int(most_similar_index)
    cursor = collection.find().skip(most_similar_index).limit(1)
    suggested_document = str(cursor[0]['_id'])
    similarity_percentage = round(similarity_score * 100, 2)
    return f"The most similar document is {suggested_document}, with a similarity score of {similarity_percentage}%."

if __name__ == '__main__':
    app.run(debug=True)
