from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
mongo = PyMongo(app)



@app.route('/')
def index():
    # user_collection = mongo.db.users
    # user_collection.insert_one({'name' : 'Anthony'})
    return \
        '<table><row>game1</row><row>game2</row><h1>Added a User!</h1></table>'






###########################
#
# from flask import Blueprint
#
# from .extensions import mongo
#
# main = Blueprint('main', __name__)
#
# @main.route('/')
# def index():
#     user_collection = mongo.db.users
#     user_collection.insert({'name': 'Anthony'})
#     return '<h1>Added a User!</h1>'