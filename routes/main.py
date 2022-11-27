from flask import Blueprint

from ..mongodb.mongo_connect import mongo

main = Blueprint('main', __name__)

@main.route('/')
def login():
    # account_collection = mongo.db.get_collection('accounts')
    # account_collection.insert_one({
    #     'username': 'panda',
    #     'email': 'panda@foo.bar',
    #     'passphrase': 'panda',
    #     'pub_key': '',
    #     'documents': [
    #         {
    #             'encrypted_link': '',
    #             'sign_reg_link': '',
    #             'sign_std_link': ''
    #         }
    #     ]
    # })
    return "Login Page!"

@main.route('/authority')
def institute_authority():
    return "Only Institute Authority Allowed"

@main.route('/student')
def student():
    return "Students Suck over here!"

@main.route('/verify')
def verifier():
    return "Please Verify Here!"