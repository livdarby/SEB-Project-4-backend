from datetime import datetime, timezone, timedelta
import pprint
from app import app, db
from models.prediction import PredictionModel
from models.user import UserModel
from models.match import MatchModel
from serpapi import GoogleSearch
from config.environment import API_KEY

with app.app_context():

    

    try:
        print("Connected to the database! 🔥")

        params = {
            "q": "manchester united",
            "api_key": API_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        matches = results.get("sports_results", {})
        matches_games = matches.get("games", [])

        matches_spotlight = matches.get("game_spotlight")

        a = []

        if matches_spotlight:
            a.append(matches_spotlight.copy())

        matches = matches_games + a
        pprint.pp(matches)

        premier_league_matches = [
            match
            for match in matches
            if match.get("tournament") == "Premier League"
            or match.get("league") == "Premier League"
        ]

        future_matches = []
        for match in premier_league_matches:
            pass

        pprint.pp(premier_league_matches)
        print("Seeding some data...")

    except Exception as e:
        print(e)
