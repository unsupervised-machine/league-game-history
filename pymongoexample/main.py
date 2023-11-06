from flask import Flask, current_app, g, request
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from models import User

import uuid
import random
from faker import Faker


# TODO: move to separate database file?
# def get_db():
#     """
#     Configuration method to return db instance
#     """
#     db = getattr(g, "_database", None)
#
#     if db is None:
#         db = g._database = PyMongo(current_app).db
#
#     return db
#
#
# # Use LocalProxy to read the global db instance with just `db`
# db = LocalProxy(get_db)

main = Flask(__name__)
main.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
mongo = PyMongo(main)

# ## get db
# db = g._database = PyMongo(main).db


@main.route('/')
def create_user():
    random_user = User(
        puuid=str(uuid.uuid4()),
        summoner_name=Faker().name(),
        profile_icon_id=random.randint(1, 200),
        summoner_level=random.randint(0, 100_000),
    )
    user_collection = mongo.db.users.insert_one(random_user)
    return str(random_user)



@main.route('/users/<string:puuid>')
def get_user_with_puuid(puuid: str):
    user_entry = mongo.db.users.find_one({"puuid": puuid})
    user = User.from_database(user_entry)
    return str(user)


# TODO: switch this function from create_user() to get_all_users()
@main.route('/users')
def get_all_users():
    # random_user = User(
    #     puuid=str(uuid.uuid4()),
    #     summoner_name=Faker().name(),
    #     profile_icon_id=random.randint(1, 200),
    #     summoner_level=random.randint(0, 100_000),
    # )
    # user_collection = mongo.db.users.insert_one(random_user)
    # return str(random_user)

    pass


# TODO: find out what to use instead of request.form (using flask) to pass in data (maybe headers?)
@main.route('/users', methods=["POST"])
def post_user():
    user = User(
        puuid=request.form["puuid"],
        summoner_name=request.form["summoner_name"],
        profile_icon_id=int(request.form["profile_icon_id"]),
        summoner_level=int(request.form["summoner_level"]),
    )
    mongo.db.users.insert_one({str(user)})
    return str(user)


main.run()

## TODO NOW
# fix /users to get all users
# fix POST call to /users correctly

# get match info
# post match info

# get a user's match history
# post a user's match history


## TODO LATER
# input parameters as headers instead of url
# learn how to setup db for mongodb properly using LocalProxy()
