import os
from flask import request, jsonify
from bson.binary import Binary
from bson.objectid import ObjectId

from ..crypto.hash import Hash
from ..crypto.signature import Signature
from ..crypto.key_generator import KeyGenerator
from ..crypto.verifiyer import Verifyer

from .mongo_connect import mongo
from ..env import UPLOAD_FOLDER, SIGNED_FOLDER

class Accounts:
    
    def login(self):

        # create password for account
        passphrase = Hash().hash(request.form.get('password').encode('utf-8'))

        # find user if exists in db 
        accounts_collection = mongo.db.get_collection('accounts')
        record = accounts_collection.find_one({ "email" : request.form.get('email')})
        if record == None:
            # create user object
            user = {
                "name": request.form.get('name'),
                "email": request.form.get('email'),
                "password": passphrase,
                "designation": request.form.get('designation'),
                "fingerprint": "",
                "documents": []
            }
            user['fingerprint'] = KeyGenerator().generate_key(name=user['name'], email=user['email'], secretkey=request.form.get('password'))

            # insert record
            accounts_collection.insert_one(user)
        else:
            if passphrase == record['password']:
                # send record as it is
                return jsonify({
                    "name": record['name'],
                    "email": record['email'],
                    "password": record['password'],
                    "designation": record['designation'],
                    "fingerprint": record['fingerprint'],
                    "documents": record['documents']
                }), 200
            else:
                return jsonify({
                    "Error": "Wrong Password"
                }), 400

        return jsonify({
            "name": user['name'],
            "email": user['email'],
            "password": user['password'],
            "designation": user['designation'],
            "fingerprint": user['fingerprint'],
            "documents": user['documents']
        }), 200

    def getkey(self):

        # params
        fp = request.form.get('fingerprint')
        passphrase = request.form.get('password')

        # retrieve keys from fingerprint
        kg = KeyGenerator()
        kg_pvt = kg.export_key(keyid=fp, pwd=passphrase, private=True)      # secret key export
        kg_pub = kg.export_key(keyid=fp)                                    # public key export

        return jsonify({
            'pub_key': kg_pub,
            'pvt_key': kg_pvt
        }), 200

    def add(self, id):
        
        # find user if exists in db 
        accounts_collection = mongo.db.get_collection('accounts')

        accounts_collection.update_one({
            'email': request.form.get('studentid')
        }, {
            '$push': {
                'documents': id
            }
        })
        
        return jsonify({
            'message': 'Successfully Updated Document to Students Account!'
        }), 200


class Documents():

    def filedata(self, filepath, filename):
        with open(filepath+filename, "rb") as f:
            data = Binary(f.read())
        f.close()
        return data

    def add(self, filename):

        # certificate name
        cert = request.form.get('certname')

        # encrypt file 
        encrypted = self.filedata(filepath=UPLOAD_FOLDER, filename=filename)

        # sign the hash of original file using fingerprint
        Signature().sign(filename=filename, password=request.form.get('password'), email=request.form.get('email'))
        signed = self.filedata(filepath=SIGNED_FOLDER, filename=filename+'.sig')

        # put the encrypted file and sign file on students documents array as object with 3 parameters
        doc = {
            'filename': filename,
            'certificate' : cert, 
            'filedata' : encrypted,
            'sig_reg' : signed,
            'sig_std' : None
        }

        # add to documents collection and get the _id from it
        documents_collection = mongo.db.get_collection('documents')
        response = documents_collection.insert_one(doc)

        # return the _id to use for users database
        return response.inserted_id

    def sign(self):
        
        # get collection
        documents_collection = mongo.db.get_collection('documents')

        # find the document and sign the hash
        doc = documents_collection.find_one({
            '_id': ObjectId(request.form.get('id'))
        })

        if(doc['sig_std'] == None):

            # save file
            stream = open(UPLOAD_FOLDER+doc['filename'], "wb")
            stream.write(doc['filedata'])
            stream.close()

            # create sign 
            Signature().sign(filename=doc['filename'], password=request.form.get('password'), email=request.form.get('email'))
            signed = self.filedata(filepath=SIGNED_FOLDER, filename=doc['filename']+'.sig')
            
            # find the document entry with same hash
            documents_collection.update_one({
                '_id': ObjectId(request.form.get('id'))
            }, {
                '$set': {
                    'sig_std': signed
                }
            })

            # delete file
            os.remove(os.path.join(UPLOAD_FOLDER, doc['filename']))
            os.remove(os.path.join(SIGNED_FOLDER, doc['filename']+'.sig'))

            return jsonify({
                'message': 'successfully signed for student using email and password!'
            }), 200

        else :
            return jsonify({
                'message' : 'document already signed!'
            }), 202

    def get(self):

        # get collection
        documents_collection = mongo.db.get_collection('documents')

        doc = documents_collection.find_one({
            '_id': ObjectId(request.form.get('id'))
        })

        return jsonify({
            'message': str(doc['filedata'], 'utf-8'),
            'signature faculty': str(doc['sig_reg'], 'utf-8'),
            'signature student': str(doc['sig_std'], 'utf-8')
        }), 200

    def verify(self, doc, _hash, designation):
        filename = doc['filename']

        # save file
        stream = open(SIGNED_FOLDER+filename+'.sig', "wb")
        stream.write(doc[designation])
        stream.close()

        # get hash after verifying
        h = Verifyer().decrypt(filename, keyid=request.form.get(designation))
        print('Hash from Verifyer: ', h)

        # delete file
        os.remove(os.path.join(SIGNED_FOLDER, filename+'.sig'))

        if h != None and str(h)[:-1] == str(_hash):
            return True
        else :
            return False

    def verify_wrapper(self):

        # get collection
        documents_collection = mongo.db.get_collection('documents')

        doc = documents_collection.find_one({
            '_id': ObjectId(request.form.get('id'))
        })

        # save file
        stream = open(UPLOAD_FOLDER+doc['filename'], "wb")
        stream.write(doc['filedata'])
        stream.close()

        # calculate hash
        stream = open(UPLOAD_FOLDER+doc['filename'], 'rb')
        _hash = Hash().hash(message=stream.read())

        print('Actual Hash of File: ', _hash)

        # delete file
        os.remove(os.path.join(UPLOAD_FOLDER, doc['filename']))

        # verify
        if self.verify(doc, _hash, 'sig_reg') and self.verify(doc, _hash, 'sig_std') : 
            return 'Verification Successfull!', 200
        else:
            return 'Verification Unsuccessfull!', 400