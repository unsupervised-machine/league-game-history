import enum

from flask import g, current_app
from flask_pymongo import PyMongo
import flask_pymongo


class GameMode(enum.Enum):
    CLASSIC = "CLASSIC"
    ARAM = "ARAM"


class Participant(dict):
    def __init__(self, puuid: str, champion_id: int, individual_position: str):
        self.puuid = puuid
        self.champion_id = champion_id
        self.individual_position = individual_position
        super().__init__({"puuid": puuid, "champion_id": champion_id, "individual_position": individual_position})


class Match(dict):
    def __init__(self, match_id: str, game_creation: int, game_duration: int, game_mode: GameMode, game_version: str, participants: list[Participant]):
        self.match_id = match_id
        self.game_creation = game_creation
        self.game_duration = game_duration
        self.game_mode = game_mode
        self.game_version = game_version
        self.participants = participants
        super().__init__({
            "match_id": match_id,
            "game_creation": game_creation,
            "game_duration": game_duration,
            "game_mode": game_mode.value,
            "game_version": game_version,
            "participants": participants,
        })


class User(dict):
    def __init__(self, puuid: str, summoner_name: str, profile_icon_id: int, summoner_level: int):
        self.puuid = puuid
        self.summoner_name = summoner_name
        self.profile_icon_id = profile_icon_id
        self.summoner_level = summoner_level
        super().__init__({
            "puuid": puuid,
            "summoner_name": summoner_name,
            "profile_icon_id": profile_icon_id,
            "summoner_level": summoner_level,
        })

    @staticmethod
    def from_database(user_entry):
        return User(
            puuid=user_entry["puuid"],
            summoner_name=user_entry["summoner_name"],
            profile_icon_id=user_entry["profile_icon_id"],
            summoner_level=user_entry["summoner_level"],
        )
