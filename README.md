# ISP-Backend
Information Security Project 


# Code 
Code can be divided into 3 Major Modules
1. Crypto Module - deals with independent cryptographic functions
2. MongoDB Module - deals with connecting to database for storage on cloud
3. Routes - deals with backend api calls and serves html pages

<i>We also have virturla frontend module which handles all the frontend code. Modules static and templates together combines as frontend module.</i>

### Crypto Module : 
1. <b>Encryptor</b> - provide filename(file present in UPLOAD_FOULDER), keyid (email of reciepent). Encrypted Document will be saved in ENCRYPTED folder.
2. <b>Hash</b> - uses SHA256 to create hash of the message (provided as argument to function)
3. <b>Key Generator</b> - generates key pair based name, email, secretkey. You can customize the key generator based on your requirement in input_data like <i> key_type, key_length, algorithm, etc.</i>
4. <b>Signature</b> - provide password for signature with private key, filename (file present in UPLOAD_FOLDER). This creates hash and signs with private key of user.
5. <b>Verifier</b> - verifies the signature against the intended user given fingerprint and filename.

### MongoDB Module : 
1. <b>Model</b> - contains logic for accounts and documents schema to be stored on Cloud database.
2. <b>Mongo Connect</b> - creates instance for the pymongo class.

### Routes Module :
<b>Main</b> - contains route for login, upload document, sign document, download document, verifying document and serve html pages based on the request.
1. <i>/registrar/</i> - returns registrar page on GET request and uploads document on POST request with all the parameters required (otherwise returns error).
2. <i>/student/</i> - returns students document ids after login on GET request and signs the document on clicking the SIGN option with POST request.
3. <i>/verify/</i> - verifies the document given document id, fingerprint of registrar and student with GET request.
4. <i>/login/</i> - redirects to new webpage once logged in on the basis of designation and creates new user if user doesn't exist already with POST request. 
5. <i>/keys/</i> - renders html page for viewing the public key of the user with GET requrest.
6. <i>/documents/ & /getkeys/ & & /verify_api/</i> - used internally within other routes.

## Login Page
<img src="Images/Login Page.png">


## Registrar Page
<img src="Images/Registrar Page.png">


## Students Page
<img src="Images/Students Page.png">


## Verifier Page
<img src="Images/Verifier Page.png">


## Verifier Alert
<img src="Images/Verifier Output.png">


# How to run the code:
Clone/download the code into a **linux** machine. There is a makefile that will do all the setup for you. For the setup, just run:
**make install**;

Then, to run the code, run **make linux** or just the last line in make linux. This starts the Flask server on localhost. Open up a browser window and navigate to localhost:3000 or 127.0.0.1:3000 to see the webpage. 
