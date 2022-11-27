from flask import request, jsonify

from ..crypto.hash import Hash
from .mongo_connect import mongo

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
                "pub_key": "",
                "documents": []
            }

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
                    "pub_key": record['pub_key'],
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
            "pub_key": user['pub_key'],
            "documents": user['documents']
        }), 200