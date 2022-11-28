import os
from flask import Blueprint, request
from werkzeug.utils import secure_filename
from bson.binary import Binary

from ..mongodb.model import Accounts
from ..crypto.signature import Signature

main = Blueprint('main', __name__)

UPLOAD_FOLDER = './crypto/uploads/'
SIGNED_FOLDER = './crypto/signed/'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def filedata(filepath, filename):
    with open(filepath+filename, "rb") as f:
        data = Binary(f.read())
    f.close()
    return data

@main.route('/', methods=['POST'])
def login():
    return Accounts().login()

@main.route('/getkeys', methods=['GET'])
def getkeys():
    return Accounts().getkey()

@main.route('/authority')
def institute_authority():
    return "Only Institute Authority Allowed"

@main.route('/authority/upload', methods=['POST'])
def upload():
    
    file = request.files['document']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file'
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # encrypt file 
        # sign the hash of original file using fingerprint
        Signature().sign(filename=filename, password=request.form.get('password'), email=request.form.get('email'))
        # put the encrypted file and sign file on students documents array as object with 3 parameters
        
        doc = {
            'filename': filename,
            'certificate' : request.form.get('certname'), 
            'filedata' : filedata(filepath='./crypto/uploads/', filename=filename),
            'sig_reg' : filedata(filepath='./crypto/signed/', filename=filename+'.sig')
        }

        res = Accounts().add(doc, request.form.get('studentid'))

        # DO NOT FORGET TO DELETE THE DOCUMENT ONCE UPLOADED AND ENCRYPTED
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        os.remove(os.path.join(SIGNED_FOLDER, filename+'.sig'))

        return res
    else:
        return 'File Not Provided Correctly!'

@main.route('/student')
def student():
    return "Students Suck over here!"

@main.route('/student/sign', methods=['POST'])
def sign():
    return Accounts().sign()

@main.route('/verify')
def verifier():
    return "Please Verify Here!"