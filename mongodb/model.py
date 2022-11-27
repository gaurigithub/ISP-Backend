from flask import request, jsonify

from ..crypto.hash import Hash
from .mongo_connect import mongo
from ..crypto.key_generator import KeyGenerator

class Accounts:
    
    def login(self):
        # check for request parameters
        print(request.form)

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
        
        # check for request parameters
        print(request.form)

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

    def update(self):
        pass