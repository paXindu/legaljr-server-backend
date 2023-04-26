import os
import glob
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


data_path = "./path"
files = glob.glob(os.path.join(data_path, "*.txt"))
docs = []
for file in files:
    with open(file, "r") as f:
        docs.append(f.read())

# Tokenize 
docs_tokenized = []
for doc in docs:
    tokens = word_tokenize(doc.lower())
    docs_tokenized.append(tokens)

# Remove stop words and punctuation
stopwords = nltk.corpus.stopwords.words("english")
docs_filtered = []
for doc in docs_tokenized:
    filtered = [word for word in doc if word not in stopwords and word.isalpha()]
    docs_filtered.append(filtered)


docs_preprocessed = []
for doc in docs_filtered:
    preprocessed = " ".join(doc)
    docs_preprocessed.append(preprocessed)

# vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(docs_preprocessed)
docs_vectorized = vectorizer.transform(docs_preprocessed)



def suggest_similar_document(document):
    
    document_tokenized = word_tokenize(document.lower())
    document_filtered = [word for word in document_tokenized if word not in stopwords and word.isalpha()]
    document_preprocessed = " ".join(document_filtered)

    document_vectorized = vectorizer.transform([document_preprocessed])

    similarity_scores = cosine_similarity(document_vectorized, docs_vectorized)

    most_similar_index = similarity_scores.argmax()
    similarity_score = similarity_scores[0][most_similar_index]

    similarity_percentage = round(similarity_score * 100, 2)

    return files[most_similar_index], similarity_percentage


with open('q.txt', 'r') as file:
    content = file.read()
sample_document = content

suggested_document, similarity_percentage = suggest_similar_document(sample_document)
print(f"The most similar document is {suggested_document}, with a similarity score of {similarity_percentage}%.")