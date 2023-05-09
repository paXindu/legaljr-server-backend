from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import PyPDF2


client = MongoClient('localhost', 27017)
db = client['pdfs']
pdf_files = db['pdf_files']


def upload_pdf():
    file = request.files['pdf']
    filename = file.filename
    filedata = file.read()

    
    reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(reader.getNumPages()):
        page = reader.getPage(page_num)
        text += page.extractText()

    # MongoDB
    pdf = {'name': filename, 'text': text}
    pdf_id = pdf_files.insert_one(pdf).inserted_id

    return jsonify({'_id': str(pdf_id)}), 201



