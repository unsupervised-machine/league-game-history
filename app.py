from typing import Any

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

from collections import OrderedDict

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



# @app.route('/summoners/search', methods=["GET", "POST"])
# def summoner_search():
#     # example usage: http://127.0.0.1:5000/summoners/search --> taran
#     form = SearchForSummoner()
#     if form.validate_on_submit():
#         summoner = {
#             "summoner_name": form.summoner_name.data
#         }
#         api_url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner["summoner_name"]}?api_key={API_KEY}'
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             filter_criteria = {'puuid': data['puuid']}
#             update_operation = {
#                 '$set': {
#                     'puuid': data['puuid'],
#                     'summoner_name': data['name'],
#                     'profile_icon_id': data['profileIconId'],
#                     'summoner_level': data['summonerLevel'],
#                     'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 }
#             }
#             mongo.db.users.update_one(filter_criteria, update_operation, upsert=True)
#             return render_template('display_summoner.html', data=data, the_title=data['name'])
#         else:
#             # Handle API error response
#             error_message = "Error fetching summoner data"
#             return {"error": error_message}, response.status_code
#     return render_template('test_form.html', form=form)



"""
TODO:
    Create a match history collection, add last 20 games of a summoner when they are searched
"""


def fetch_account_info_summoner(summoner: str) -> dict | None:
    api_url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={API_KEY}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 OK
    except requests.exceptions.RequestException as e:
        # Handle exceptions for failed HTTP request
        print(f"HTTP Request Error: {e}")
        return None
    try:
        data = response.json()
    except ValueError as e:
        # Handle exceptions for JSON parsing errors
        print(f"JSON Parsing Error: {e}")
        return None
    return data


def fetch_match_history_puuid(puuid: str, num_games=20) -> list | None:
    api_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num_games}&api_key={API_KEY}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 OK
    except requests.exceptions.RequestException as e:
        # Handle exceptions for failed HTTP request
        print(f"HTTP Request Error: {e}")
        return None
    try:
        data = response.json()
    except ValueError as e:
        # Handle exceptions for JSON parsing errors
        print(f"JSON Parsing Error: {e}")
        return None
    return data


def fetch_match_details(match_id: str) -> dict | None:
    api_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception if the response status code is not 200 OK
    except requests.exceptions.RequestException as e:
        # Handle exceptions for failed HTTP request
        print(f"HTTP Request Error: {e}")
        return None
    try:
        match_data = response.json()
    except ValueError as e:
        # Handle exceptions for JSON parsing errors
        print(f"JSON Parsing Error: {e}")
        return None
    return match_data


def get_champion_id(puuid: str, match_data: dict) -> int:
    # can we display champion skin rather than base champion icon?
    # looked it up answer to above is no...
    player_index = match_data["metadata"]["participants"].index(puuid)
    champion_id = match_data["info"]["participants"][player_index]["championId"]
    return champion_id


def get_win_or_loss(puuid:str, match_data: dict) -> bool:
    player_index = match_data["metadata"]["participants"].index(puuid)
    return match_data["info"]["participants"][player_index]["win"]


def get_players(match_data: dict):
    pass

def get_game_mode(match_data: dict) -> str:
    return match_data["info"]["gameMode"]


def get_kills_death_assists(puuid:str, match_data: dict) -> (int, int, int):
    player_index = match_data["metadata"]["participants"].index(puuid)
    kills = match_data["info"]["participants"][player_index]["kills"]
    deaths = match_data["info"]["participants"][player_index]["deaths"]
    assists = match_data["info"]["participants"][player_index]["assists"]
    return kills, deaths, assists


def get_minions_killed(puuid:str, match_data: dict) -> int:
    return match_data["info"]["participants"][player_index]["totalMinionsKilled"]


def get_damaged_dealt(puuid:str, match_data: dict) -> int:
    return match_data["info"]["participants"][player_index]["totalDamageDealt"]


def get_final_items(puuid:str, match_data: dict) -> (int, int, int, int, int, int, int):
    player_index = match_data["metadata"]["participants"].index(puuid)
    item_0 = match_data["info"]["participants"][player_index]["item0"]
    item_1 = match_data["info"]["participants"][player_index]["item1"]
    item_2 = match_data["info"]["participants"][player_index]["item2"]
    item_3 = match_data["info"]["participants"][player_index]["item3"]
    item_4 = match_data["info"]["participants"][player_index]["item4"]
    item_5 = match_data["info"]["participants"][player_index]["item5"]
    item_6 = match_data["info"]["participants"][player_index]["item6"]
    return item_0, item_1, item_2, item_3, item_4, item_5, item_6


@app.route('/summoners/search', methods=["GET", "POST"])
def summoner_search():
    # example usage: http://127.0.0.1:5000/summoners/search --> taran
    form = SearchForSummoner()
    if form.validate_on_submit():
        summoner_name = form.summoner_name.data
        account_info = fetch_account_info_summoner(summoner_name)
        # can only handle 20 match_ids for now
        match_history_ids = fetch_match_history_puuid(account_info['puuid'])[:20]
        # supplementary_match_info is used for html won't be saved into database
        supplementary_match_info = OrderedDict()
        for idx, match_id in enumerate(match_history_ids):
            match_data = fetch_match_details(match_id=match_id)
            champion_id = get_champion_id(puuid=account_info['puuid'], match_data=match_data)
            win_bool = get_win_or_loss(puuid=account_info['puuid'], match_data=match_data)
            supplementary_match_info[match_id] = {
                'index': idx,
                'match_id': match_id,
                'champion_id': champion_id,
                'win_bool': win_bool
            }

        filter_criteria = {'puuid': account_info['puuid']}
        update_operation = {
            '$set': {
                'puuid': account_info['puuid'],
                'summoner_name': account_info['name'],
                'profile_icon_id': account_info['profileIconId'],
                'summoner_level': account_info['summonerLevel'],
                'recent_matches': match_history_ids,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        mongo.db.users.update_one(filter_criteria, update_operation, upsert=True)
        return render_template('display_summoner.html',
                               account_info=account_info,
                               supplementary_match_info=supplementary_match_info
                               )
    return render_template('test_form.html', form=form)



"""
TODO:
    Create auto update high elo summoner list.
        Delete existing table of high elo summoners.
        request new list of high elo players and add it to database
            
"""




if __name__ == '__main__':
    app.run(debug=True)
