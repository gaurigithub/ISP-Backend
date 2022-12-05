import os
from ..env import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, SIGNED_FOLDER
from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import json

from ..mongodb.model import Accounts, Documents

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
WEBSITE PAGE ROUTES
'''
@main.route('/', methods=['GET'])
def landing_page():
    return render_template('login.html')

@main.route('/registrar/', methods=['GET', 'POST'])
def registrar():
    message = request.cookies.get('message', '')
    if(request.method == 'GET'):
        print(message)
        if(json.loads(message).get('Error', '') != ''):
            return "Invalid password/email. Please try again"

        if(message != ''):
            message = json.loads(message)
            print(message)
        return render_template('registrar.html', password=message['password'], key_fingerprint=message['fingerprint'])

    elif(request.method == 'POST'):
        print(request.form)
        message = json.loads(message)
        sent_request = json.loads(request.cookies.get('message'))
        sent_request['certname'] = request.form['certname']
        sent_request['studentid'] = request.form['studentid']
        sent_request['password'] = request.form['password']
        
        file = request.files['document']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        response = ""
        if file.filename == '':
            response = 'No selected file'
            
        if file: # and allowed_file(file.filename):
            # save files securely
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            # print(f"\n\nFile saved at {os.path.join(UPLOAD_FOLDER, filename)}\n\n")
            # insert document in documents collection and push to account
            id = Documents().add(sent_request, filename=filename)
            res = Accounts().add(sent_request, id)

            # DO NOT FORGET TO DELETE THE DOCUMENT ONCE UPLOADED AND ENCRYPTED
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
            os.remove(os.path.join(SIGNED_FOLDER, filename+'.sig'))

            response = json.loads(res[0].response[0])['message']
        else:
            response = 'File Not Provided Correctly!'
        
        print(response)
        return render_template('registrar.html', password=message['password'], key_fingerprint=message['fingerprint'], flash="true", print_m=response)

@main.route('/student/', methods=['GET', 'POST'])
def student():
    if(request.method == 'GET'):
        message = request.cookies.get('message', '')
        if(json.loads(message).get('Error', '') != ''):
            return "Invalid password/email. Please try again"

        if(message != ''):
            message = json.loads(message)
            print(message)
            print(message['documents'])

            num_documents = len(message['documents'])
            for document in message['documents']:
                print(document['certificate'])
                print(document['id'])

        return render_template('student_page.html', flash="false", print_m="", message=message['documents'])
    
    elif(request.method == 'POST'):
        sent_request = json.loads(request.cookies.get('message'))
        id_param = json.loads(request.form['docid'])
        type_of_request = id_param['type']

        if(type_of_request == "sign"):
            sent_request['id'] = id_param['docid']
            sent_request['password'] = request.form['passphrase']

            response = Documents().sign(sent_request)
            response = json.loads(response[0].response[0])

            message = json.loads(request.cookies.get('message', ''))['documents']
            return render_template('student_page.html', flash="true", print_m=response['message'], message=message)
        
        elif(type_of_request == "download"):
            redirected = redirect(url_for('main.download'))
            redirected.set_cookie('docid', id_param['docid'])
            return redirected

@main.route('/verify/', methods=['GET'])
def verifier():
    message = request.cookies.get('message', '')
    print(message)
    if(json.loads(message).get('Error', '') != ''):
        return "Invalid password/email. Please try again"

    if(message != ''):
        message = json.loads(message)
        print(message)
    
    return render_template('verifier.html', status=100)


'''
API ROUTES
'''
# name, email, password, designation
@main.route('/login', methods=['POST', 'GET'])
def login():
    name = request.form['name']
    email = request.form['email']
    passphrase = request.form['password']
    designation = request.form['designation']

    message = Accounts().login(request)
    response = json.loads(message[0].response[0])
    
    if(response.get('Error', '') != ''):
        return render_template('login.html', failed="true")

    if(designation == 'registrar'):
        redirected = redirect(url_for('main.registrar'))
    elif(designation == 'student'):
        redirected = redirect(url_for('main.student'))
    elif(designation == 'verifier'):
        redirected = redirect(url_for('main.verifier'))
        
    redirected.set_cookie('message', message[0].response[0])
    return redirected

@main.route('/keys', methods=['GET'])
def keys():
    return render_template('getkey.html')

# fingerprint, password (original)
@main.route('/getkeys', methods=['POST'])
def getkeys():
    message, _ = Accounts().getkey()
    return render_template('showkey.html', pub_key=message['pub_key'], pvt_key=message['pvt_key'])

# id (document _id)
@main.route('/document', methods=['GET'])
def download():
    return Documents().get(request.cookies.get('docid', ''))

# id (document id), sig_reg (fingerprint of registrar), sig_std (fingerprint of student)
@main.route('/verify_api/', methods=['POST', 'GET'])
def verifying_api():
    msg, status = Documents().verify_wrapper()
    return render_template('verifier.html', msg=msg, status=status)
