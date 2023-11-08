from flask import Flask, current_app, g, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from forms import CreateUserForm

from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from models import User

import uuid
import random
from faker import Faker

# TODO Implement Secrets
# import secrets
# foo = secrets.token_urlsafe(16)
# app.secret_key = foo



# TODO: ( later) move to separate database file?
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

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
mongo = PyMongo(app)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

# ## get db
# db = g._database = PyMongo(app).db


@app.route('/users/test_form', methods=["GET", "POST"])
def create_random_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        random_user = {
            "puuid": form.puuid.data,
            "summoner_name": form.summoner_name.data,
            "profile_icon_id": form.profile_icon_id.data,
            "summoner_level": form.summoner_level.data,
        }
        user_collection = mongo.db.users.insert_one(random_user)
        return redirect(url_for('get_user_by_puuid', puuid=form.puuid.data))
    form.puuid.data = str(uuid.uuid4())
    form.summoner_name.data = Faker().name()
    form.profile_icon_id.data = random.randint(1, 200)
    form.summoner_level.data = random.randint(0, 100_000)
    return render_template('test_form.html', form=form)


@app.route('/users/<string:puuid>')
def get_user_by_puuid(puuid: str):
    # example usage:
    #   http://127.0.0.1:5000/users/f173c145-d44b-4ebb-8c46-f78e94379ab0
    user_entry = mongo.db.users.find_one({"puuid": puuid})
    user = User.from_database(user_entry)
    return str(user)


# @app.route('/users/all', method=['GET'])
# def get_all_users():
#     # example usage:
#     #   http://127.0.0.1:5000/users/all
#     all_users_entry = mongo.db.users.find()
#     all_users = []
#     for x in all_users_entry:
#         # print(x)
#         all_users.append(x)
#     return str(all_users)


# TODO: find out what to use instead of request.form (using flask) to pass in data (maybe headers?)
@app.route('/users', methods=["POST"])
def post_user():
    user = User(
        puuid=request.form["puuid"],
        summoner_name=request.form["summoner_name"],
        profile_icon_id=int(request.form["profile_icon_id"]),
        summoner_level=int(request.form["summoner_level"]),
    )
    mongo.db.users.insert_one({str(user)})
    return str(user)


app.run()

## TODO NOW
# fix POST call to /users correctly

# get match info
# post match info

# get a user's match history
# post a user's match history


## TODO LATER
# input parameters as headers instead of url
# learn how to setup db for mongodb properly using LocalProxy()
