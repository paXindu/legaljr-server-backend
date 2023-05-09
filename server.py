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
user=db['user']

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

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    new_user = {
        'username': data['username'],
        'password': data['password'],
        'email': data['email']
    }
    result = user.insert_one(new_user)
    return f'User {data["username"]} created with id {result.inserted_id}'

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    users = user.find_one({'username': username, 'password': password})
    
    if users:
        return jsonify({'success': True, 'message': 'Logged in successfully!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'})


if __name__ == '__main__':
    app.run(debug=True)