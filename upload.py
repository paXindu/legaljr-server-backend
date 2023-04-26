from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client['pdfs']
pdf_files = db['pdf_files']

@app.route('/pdfs', methods=['POST'])
def upload_pdf():
    file = request.files['pdf']
    filename = file.filename
    filedata = file.read()

    # Extract text from the PDF file
    reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(reader.getNumPages()):
        page = reader.getPage(page_num)
        text += page.extractText()

    # Store the text file in MongoDB
    pdf = {'name': filename, 'text': text}
    pdf_id = pdf_files.insert_one(pdf).inserted_id

    return jsonify({'_id': str(pdf_id)}), 201

@app.route('/pdfs/<id>', methods=['GET'])
def get_pdf(id):
    pdf = pdf_files.find_one({'_id': ObjectId(id)})
    if pdf:
        return pdf['text']
    else:
        return jsonify({'error': 'PDF not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
