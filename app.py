from flask import Flask, current_app, g, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from forms import CreateUserForm, SearchForSummoner

from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from models import User

from datetime import datetime

import requests

from configparser import ConfigParser
config = ConfigParser()
config.read('config/keys_config.cfg')






app = Flask(__name__)
API_KEY = config.get('riot_games', 'api_key')
app.secret_key = config.get('csrf', 'secret_key')
app.config['MONGO_URI'] = config.get('mongo', 'db_uri')
mongo = PyMongo(app)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


@app.route('/')
def status_check():
    message = 'app is running!'
    print(message)
    return message

@app.route('/users/<string:puuid>')
def get_user_by_puuid(puuid: str):
    # example usage:
    #   http://127.0.0.1:5000/users/f173c145-d44b-4ebb-8c46-f78e94379ab0
    user_entry = mongo.db.users.find_one({"puuid": puuid})
    user = User.from_database(user_entry)
    return str(user)


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


"""
TODO:
    When someone searches for a summoner, update that summoners info in our database, if it doesnt exist add it to database
"""

# instead of just printing raw json let's put the output in a nice template
# just find and display summoner
# instead o
@app.route('/summoners/search', methods=["GET", "POST"])
def summoner_search():
    # example usage: http://127.0.0.1:5000/summoners/search --> taran
    form = SearchForSummoner()
    if form.validate_on_submit():
        summoner = {
            "summoner_name": form.summoner_name.data
        }
        api_url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner["summoner_name"]}?api_key={API_KEY}'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            filter_criteria = {'puuid': data['puuid']}
            update_operation = {
                '$set': {
                    'puuid': data['puuid'],
                    'summoner_name': data['name'],
                    'profile_icon_id': data['profileIconId'],
                    'summoner_level': data['summonerLevel'],
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            mongo.db.users.update_one(filter_criteria, update_operation, upsert=True)
            return render_template('display_summoner.html', data=data, the_title=data['name'])
        else:
            # Handle API error response
            error_message = "Error fetching summoner data"
            return {"error": error_message}, response.status_code
    return render_template('test_form.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
