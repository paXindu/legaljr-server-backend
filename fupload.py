from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import PyPDF2


client = MongoClient('localhost', 27017)
db = client['pdfs']
pdf_files = db['pdf_files']
import chardet
import io



def upload_pdf():
    file = request.files['pdf']
    filename = file.filename
    filedata = file.read()

    filedata_encoding = chardet.detect(filedata)['encoding']
    
    reader = PyPDF2.PdfFileReader(io.BytesIO(filedata), strict=False)
    text = ''
    for page_num in range(reader.getNumPages()):
        page = reader.getPage(page_num)
        text += page.extractText().encode('iso-8859-1', 'ignore').decode('utf-8', 'ignore')


    # MongoDB
    pdf = {'name': filename, 'text': text}
    pdf_id = pdf_files.insert_one(pdf).inserted_id

    return jsonify({'_id': str(pdf_id)}), 201



