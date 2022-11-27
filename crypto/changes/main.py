from flask import Flask, render_template, request
import os
from message.hash import Hash
from message.encrypt import Encryptor
from message.decrypt import Decryptor
app = Flask(__name__)

temp_file_storage_location = os.getcwd() + '/documents'
	
@app.route('/upload', methods = ['POST'])
def upload_file():
    # Get the request
    f = request.files['file']   
    key_id = request.form['keyid']
    passphrase = request.form['passphrase']
    print(f"The key id being used is: {key_id}")

    # Find out the directory to store the files (temporarily)
    if(not os.path.isdir(temp_file_storage_location)):
        print(temp_file_storage_location)
        os.mkdir(temp_file_storage_location)

    # Save the file
    f.save(os.path.join(temp_file_storage_location, f.filename))

    # Sign the hash of this file using Private key
    e = Encryptor()
    signed_hash = e.encrypt(f, key_id, passphrase=passphrase)

    # d = Decryptor()
    # d.decrypt(f, key_id)

    return "Success"

		
if __name__ == '__main__':
   app.run(debug = True)