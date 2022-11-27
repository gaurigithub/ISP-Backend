from flask import Blueprint

from ..mongodb.model import Accounts
from ..mongodb.mongo_connect import mongo

main = Blueprint('main', __name__)

@main.route('/', methods=['POST'])
def login():
    return Accounts().login()

@main.route('/getkeys', methods=['GET'])
def getkeys():
    return Accounts().getkey()

@main.route('/authority')
def institute_authority():
    return "Only Institute Authority Allowed"

@main.route('/student')
def student():
    return "Students Suck over here!"

@main.route('/verify')
def verifier():
    return "Please Verify Here!"