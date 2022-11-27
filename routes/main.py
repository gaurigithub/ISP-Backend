import os
from flask import Blueprint, request
from werkzeug.utils import secure_filename

from ..mongodb.model import Accounts

main = Blueprint('main', __name__)

UPLOAD_FOLDER = './crypto/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['POST'])
def login():
    return Accounts().login()

@main.route('/getkeys', methods=['GET'])
def getkeys():
    return Accounts().getkey()

@main.route('/upload', methods=['POST'])
def upload():
    
    file = request.files['document']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file'
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'File Saved to Uploads!'

    # DO NOT FORGET TO DELETE THE DOCUMENT ONCE UPLOADED AND ENCRYPTED
    return 'Uploaded Successfully!'

@main.route('/authority')
def institute_authority():
    return "Only Institute Authority Allowed"

@main.route('/student')
def student():
    return "Students Suck over here!"

@main.route('/verify')
def verifier():
    return "Please Verify Here!"