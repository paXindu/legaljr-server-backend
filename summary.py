

from flask import Flask
from bson.objectid import ObjectId
from flask_cors import CORS
from pymongo import MongoClient
from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
import numpy as np

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client['pdfs']
pdf_files = db['pdf_files']

nlp = English()
nlp.add_pipe("sentencizer")

@app.route('/pdfs/<id>', methods=['GET'])
def get_pdf(id):
    pdf = pdf_files.find_one({'_id': ObjectId(id)})
    if pdf:
        text = pdf['text']
        doc = nlp(text.replace("\n", ""))
        sentences = [sent.text.strip() for sent in doc.sents]
        sentence_indices = {k: v for v, k in enumerate(sentences)}

        tfidf = TfidfVectorizer(min_df=2, max_features=None, strip_accents='unicode', 
                                analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1, 3), 
                                use_idf=1, smooth_idf=1, sublinear_tf=1, stop_words='english')
        tfidf.fit(sentences)
        sentence_vectors = tfidf.transform(sentences)

        sentence_scores = np.array(sentence_vectors.sum(axis=1)).ravel()
        N = 3
        top_sentences = [sentences[ind] for ind in np.argsort(sentence_scores, axis=0)[::-1][:N]]

        mapped_top_sentences = [(sent, sentence_indices[sent]) for sent in top_sentences]
        ordered_top_sentences = [sent for sent, index in sorted(mapped_top_sentences, key=lambda x: x[1])]

        summary = " ".join(ordered_top_sentences)

        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'PDF not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
