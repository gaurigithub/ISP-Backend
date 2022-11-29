import os
from ..env import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, SIGNED_FOLDER
from flask import Blueprint, request
from werkzeug.utils import secure_filename

from ..mongodb.model import Accounts, Documents

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# name, email, password, designation
@main.route('/', methods=['POST'])
def login():
    return Accounts().login()

# fingerprint, password (original)
@main.route('/getkeys', methods=['GET'])
def getkeys():
    return Accounts().getkey()

@main.route('/authority')
def institute_authority():
    return "Only Institute Authority Allowed"

# document(file), email of registrar, password (original), studentid (email of student), certname (name for certificate)
@main.route('/authority/upload', methods=['POST'])
def upload():
    
    file = request.files['document']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file'
        
    if file and allowed_file(file.filename):
        # save files securely
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # insert document in documents collection and push to account
        id = Documents().add(filename=filename)
        res = Accounts().add(id)

        # DO NOT FORGET TO DELETE THE DOCUMENT ONCE UPLOADED AND ENCRYPTED
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        os.remove(os.path.join(SIGNED_FOLDER, filename+'.sig'))

        return res
    else:
        return 'File Not Provided Correctly!'

@main.route('/student')
def student():
    return "Students Suck over here!"

# id (document id retrieved from documents array of student account), email (student's email), password (original)
@main.route('/student/sign', methods=['POST'])
def sign():
    return Documents().sign()

# id (document _id)
@main.route('/document', methods=['GET'])
def doc():
    return Documents().get()

# id (document id), sig_reg (fingerprint of registrar), sig_std (fingerprint of student)
@main.route('/verify', methods=['GET'])
def verifier():
    return Documents().verify_wrapper()