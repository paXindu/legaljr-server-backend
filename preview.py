from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS



client = MongoClient('localhost', 27017)
db = client['pdfs']
pdf_files = db['pdf_files']

def get_pdf(id):
    pdf = pdf_files.find_one({'_id': ObjectId(id)})
    if pdf:
        return pdf['text']
    else:
        return jsonify({'error': 'PDF not found'}), 404