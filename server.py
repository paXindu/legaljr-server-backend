from flask import Flask
from bson.objectid import ObjectId
from flask_cors import CORS
from pymongo import MongoClient
from flask import Flask, jsonify, request
from summary import get_summary
from compare import get_all_files
from fupload import upload_pdf
from preview import get_pdf



app = Flask(__name__)
CORS(app, )

client = MongoClient('localhost', 27017)
db = client['pdfs']
pdf_files = db['pdf_files']

@app.route('/pdfs', methods=['POST'])
def fileupload():
    return upload_pdf()

@app.route('/pdfs/<id>', methods=['GET'])
def preview(id):
    return get_pdf(id)

@app.route('/pdfs/summary/<id>', methods=['GET'])
def summary(id):
    return get_summary(id)


@app.route('/files/<id>')
def compare(id):
    
    document = pdf_files.find_one({'_id': ObjectId(id)})
    if document is None:
        return 'Document not found' 
    text = document.get('text')
    return get_all_files(text)

@app.route('/doc/<id>')
def documents(id):
    document = pdf_files.find_one({'_id': ObjectId(id)})
    if document is None:
        return 'Document not found' 
    text = document.get('text')
    return text


if __name__ == '__main__':
    app.run(debug=True)