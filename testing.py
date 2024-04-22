import pprint
from datetime import datetime, timedelta, timezone
from serpapi import GoogleSearch
from app import db, app
from models.match import MatchModel

with app.app_context():

    todays_date = datetime.now(timezone.utc)
    # todays_date_string = (todays_date).strftime("%a, %d %b %Y %H:%M:%S GMT")

    premier_league_clubs = [
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton & Hove Albion",
        "Burnley",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Liverpool",
        "Luton Town",
        "Manchester City",
        "Manchester United",
        "Newcastle United",
        "Nottingham Forest",
        "Sheffield United",
        "Tottenham Hotspur",
        "West Ham United",
        "Wolverhampton Wanderers",
    ]

    for club in premier_league_clubs:

        params = {
                    "q": club,
                    "api_key": "",
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

        print("MATCHES")
        pprint.pp(matches)

        def formatted_date(string):
            if "yesterday" in string or "Yesterday" in string:
                return (todays_date - (timedelta(days=1))).strftime("%a, %d %b %Y %H:%M:%S GMT")
            if "today" in string.lower():
                return (todays_date).strftime("%a, %d %b %Y %H:%M:%S GMT")
            if "tomorrow" in string.lower():
                return (todays_date + (timedelta(days=1))).strftime("%a, %d %b %Y %H:%M:%S GMT")
            elif "," in string:
                return (
                    datetime.strptime(string, "%a, %b %d")
                    .strftime("%a, %d %b %Y %H:%M:%S GMT")
                    .replace("1900", "2024")
                )
            return (
                datetime.strptime(string, "%b %d")
                .strftime("%a, %d %b %Y %H:%M:%S GMT")
                .replace("1900", "2024")
            )

        def format_string_to_datetime(string):
            format_string = "%a, %d %b %Y %H:%M:%S %Z"
            return datetime.strptime(string, format_string).astimezone(timezone.utc)

        print("CLEANED DATA FROM API -----------------------")
        pprint.pp(matches)
        print(len(matches))

        filtered_matches = []
        filtered_by_league = []
        for data in matches:
            if "tournament" in data:
                if data["tournament"].lower() == "premier league":
                    filtered_by_league.append(data)
            if "league" in data:
                if data["league"].lower() == "premier league":
                    filtered_by_league.append(data)

        for data in filtered_by_league:

            filtered_teams = []

            for team in data["teams"]:
                team_info = {"name": team["name"]}
                if "score" in team:
                    team_info["score"] = team["score"]
                filtered_teams.append(team_info)

            filtered_match = {
                "date": formatted_date(data["date"]),
                "teams": filtered_teams,
            }
            if format_string_to_datetime(filtered_match["date"]) > (todays_date):
                filtered_matches.append(filtered_match)

        print("FILTERED MATCHES FOR DB ----------------------")
        pprint.pp(filtered_matches)
        print(len(filtered_matches))

        def transform_to_model(item):
            match_date = item["date"]
            team_one_name = item["teams"][0]["name"]
            team_two_name = item["teams"][1]["name"]

            model = {
                "match_date": match_date,
                "team_one_name": team_one_name,
                "team_one_score": None,
                "team_two_name": team_two_name,
                "team_two_score": None,
                "date_created": datetime.now(timezone.utc),
            }

            return model

        match_models = []
        for filtered_match in filtered_matches:
            match_model_data = transform_to_model(filtered_match)
            match_model = MatchModel(**match_model_data)
            match_models.append(match_model)
        
        for match_model in match_models:
            db.session.add(match_model)

        db.session.commit()
        # print(todays_date)
