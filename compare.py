from pymongo import MongoClient
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


client = MongoClient('localhost', 27017)
db = client.pdfs
collection = db.pdf_files

# Tokenize
docs = []
stopwords = nltk.corpus.stopwords.words("english")
for file in collection.find():
    tokens = word_tokenize(file['text'].lower())
    filtered = [word for word in tokens if word not in stopwords and word.isalpha()]
    preprocessed = " ".join(filtered)
    docs.append(preprocessed)

# Vectorize 
vectorizer = TfidfVectorizer()
vectorizer.fit(docs)
docs_vectorized = vectorizer.transform(docs)


def get_all_files(text, top_n=3):

    print(text)

    text_tokenized = word_tokenize(text.lower())
    text_filtered = [word for word in text_tokenized if word not in stopwords and word.isalpha()]
    text_preprocessed = " ".join(text_filtered)

    text_vectorized = vectorizer.transform([text_preprocessed])

    similarity_scores = cosine_similarity(text_vectorized, docs_vectorized)
    similarity_scores = similarity_scores[0]

    top_n_indices = np.argsort(similarity_scores)[-top_n:]
    top_n_indices = top_n_indices[::-1]

    similar_documents = []
    for i in top_n_indices:
        cursor = collection.find().skip(int(i)).limit(1)
        suggested_document = str(cursor[0]['_id'])
        similarity_percentage = round(similarity_scores[i] * 100, 2)
        similar_documents.append((suggested_document, similarity_percentage))

    output = ""
    for doc, sim in similar_documents:
        output += f"Document {doc} -Similarity {sim},"
    output = output.rstrip(",")  

    return output
