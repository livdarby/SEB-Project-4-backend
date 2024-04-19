import pprint
from datetime import datetime, timedelta, timezone

todays_date = datetime.now(timezone.utc)

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
            .strftime("%a, %d %b %Y %H:%M:%S GMT").replace('1900', '2024')
        )
    return datetime.strptime(string, "%b %d").strftime("%a, %d %b %Y %H:%M:%S GMT").replace('1900', '2024')

all_data = [
    {
        "tournament": "FA Cup",
        "stage": "Semi-Finals",
        "stadium": "Wembley Stadium",
        "date": "Sun, Apr 21",
        "time": "10:30 AM",
        "teams": [
            {
                "name": "Coventry",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a45f1110f165c8be32439ba9b23e5277d9d36b1bdd0da7661a9851177c114ad0f4.png",
            },
            {
                "name": "Man United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a45f1110f165c8be323b861604f85a08feb71b378df9f98eb26d998c99c0256ecb.png",
            },
        ],
    },
    {
        "tournament": "FA Cup",
        "stage": "Semi-Finals",
        "stadium": "Wembley Stadium",
        "date": "Sun, Apr 14",
        "time": "10:30 AM",
        "teams": [
            {
                "name": "REMOVE",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a45f1110f165c8be32439ba9b23e5277d9d36b1bdd0da7661a9851177c114ad0f4.png",
            },
            {
                "name": "REMOVE",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a45f1110f165c8be323b861604f85a08feb71b378df9f98eb26d998c99c0256ecb.png",
            },
        ],
    },
    {
        "tournament": "FA Cup",
        "stage": "Semi-Finals",
        "stadium": "Wembley Stadium",
        "date": "Tomorrow",
        "time": "10:30 AM",
        "teams": [
            {
                "name": "uPDATE",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a45f1110f165c8be32439ba9b23e5277d9d36b1bdd0da7661a9851177c114ad0f4.png",
            },
            {
                "name": "uPDATE",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a45f1110f165c8be323b861604f85a08feb71b378df9f98eb26d998c99c0256ecb.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Old Trafford",
        "date": "Wed, Apr 24",
        "time": "3:00 PM",
        "teams": [
            {
                "name": "Man United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4cf73b07d3ec663c25359cd00014fd57fb67eea0b952b4763c47793460bce1316.png",
            },
            {
                "name": "Sheffield United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4cf73b07d3ec663c2fcd726ce269c158a794171e3a1056b8396ed5181a163172e.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Old Trafford",
        "date": "Sat, Apr 27",
        "time": "10:00 AM",
        "teams": [
            {
                "name": "Man United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a416c281653995ac4759588b52d1b226c9fac9d40e90facd663d09fbaf6eacc099.png",
            },
            {
                "name": "Burnley",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a416c281653995ac47c9bdecbe25b995d4f2fb574b1ec14e0fa626b3e530c9a45d.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Vitality Stadium",
        "status": "FT",
        "date": "Sat, Apr 13",
        "video_highlights": {
            "link": "https://www.youtube.com/watch?v=3IVJFv8Cmf8&feature=onebox",
            "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4e5b23a0fdffffc40bde82a97b992d235a6443ea9a470a1e0e015bb06b0e15da21379cf7d70fed09c.jpeg",
            "duration": "13:26",
        },
        "teams": [
            {
                "name": "Bournemouth",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4d0ba736d1f6499bf5d58c134191963486c61d4f106412ded23b56aba927ada77.png",
            },
            {
                "name": "Man United",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4d0ba736d1f6499bfa1bb5665a557858cd54a062ae8b1c0c7ebd6f1e6cc69768b.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Old Trafford",
        "status": "FT",
        "date": "Sun, Apr 7",
        "video_highlights": {
            "link": "https://www.youtube.com/watch?v=cqyicx_NobM&feature=onebox",
            "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a410f5fbd37ecd44d155c75091b89664cc2f2f58138fd01856985df0e44e9a1d66351ef5d91faaafac.jpeg",
            "duration": "15:43",
        },
        "teams": [
            {
                "name": "Man United",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4e495aa66563657078ceea59f14f45ffe886b3fa245593c71a41cf260cc0ec161.png",
            },
            {
                "name": "Liverpool",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4e495aa66563657078d28065c67ab367035d1d8ec31a262d162d9f8b9e6a8446d.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Stamford Bridge",
        "status": "FT",
        "date": "Apr 4",
        "video_highlights": {
            "link": "https://www.youtube.com/watch?v=1XxOFv46FtY&feature=onebox",
            "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a42493348d39f521363230c5575f632ba88ae71946327ee4fce25d14367baedbfb769f0a849d5b30f9.jpeg",
            "duration": "14:33",
        },
        "teams": [
            {
                "name": "Chelsea",
                "score": "4",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4624384ba5fc86ba22871435707ef63458f6c12932ea25c6675cc1c172b9eec90.png",
            },
            {
                "name": "Man United",
                "score": "3",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4624384ba5fc86ba23f7a980d7c34ce7afa5d8f24d03693fae5f3f2266b518a18.png",
            },
        ],
    },
]
[
    {
        "tournament": "Premier League",
        "stadium": "Old Trafford",
        "date": "Wed, Apr 24",
        "time": "3:00 PM",
        "teams": [
            {
                "name": "Man United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4cf73b07d3ec663c25359cd00014fd57fb67eea0b952b4763c47793460bce1316.png",
            },
            {
                "name": "Sheffield United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4cf73b07d3ec663c2fcd726ce269c158a794171e3a1056b8396ed5181a163172e.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Old Trafford",
        "date": "Sat, Apr 27",
        "time": "10:00 AM",
        "teams": [
            {
                "name": "Man United",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a416c281653995ac4759588b52d1b226c9fac9d40e90facd663d09fbaf6eacc099.png",
            },
            {
                "name": "Burnley",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a416c281653995ac47c9bdecbe25b995d4f2fb574b1ec14e0fa626b3e530c9a45d.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Vitality Stadium",
        "status": "FT",
        "date": "Sat, Apr 13",
        "video_highlights": {
            "link": "https://www.youtube.com/watch?v=3IVJFv8Cmf8&feature=onebox",
            "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4e5b23a0fdffffc40bde82a97b992d235a6443ea9a470a1e0e015bb06b0e15da21379cf7d70fed09c.jpeg",
            "duration": "13:26",
        },
        "teams": [
            {
                "name": "Bournemouth",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4d0ba736d1f6499bf5d58c134191963486c61d4f106412ded23b56aba927ada77.png",
            },
            {
                "name": "Man United",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4d0ba736d1f6499bfa1bb5665a557858cd54a062ae8b1c0c7ebd6f1e6cc69768b.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Old Trafford",
        "status": "FT",
        "date": "Sun, Apr 7",
        "video_highlights": {
            "link": "https://www.youtube.com/watch?v=cqyicx_NobM&feature=onebox",
            "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a410f5fbd37ecd44d155c75091b89664cc2f2f58138fd01856985df0e44e9a1d66351ef5d91faaafac.jpeg",
            "duration": "15:43",
        },
        "teams": [
            {
                "name": "Man United",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4e495aa66563657078ceea59f14f45ffe886b3fa245593c71a41cf260cc0ec161.png",
            },
            {
                "name": "Liverpool",
                "score": "2",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4e495aa66563657078d28065c67ab367035d1d8ec31a262d162d9f8b9e6a8446d.png",
            },
        ],
    },
    {
        "tournament": "Premier League",
        "stadium": "Stamford Bridge",
        "status": "FT",
        "date": "Apr 4",
        "video_highlights": {
            "link": "https://www.youtube.com/watch?v=1XxOFv46FtY&feature=onebox",
            "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a42493348d39f521363230c5575f632ba88ae71946327ee4fce25d14367baedbfb769f0a849d5b30f9.jpeg",
            "duration": "14:33",
        },
        "teams": [
            {
                "name": "Chelsea",
                "score": "4",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4624384ba5fc86ba22871435707ef63458f6c12932ea25c6675cc1c172b9eec90.png",
            },
            {
                "name": "Man United",
                "score": "3",
                "thumbnail": "https://serpapi.com/searches/66221221382427e903a68c95/images/6a6244e66da8d08c4476a96d950dc8a4624384ba5fc86ba23f7a980d7c34ce7afa5d8f24d03693fae5f3f2266b518a18.png",
            },
        ],
    },
]

print(len(all_data))

filtered_matches = []
for data in all_data:

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
    if filtered_match['date'] > (todays_date).strftime("%a, %d %b %Y %H:%M:%S GMT"):
        filtered_matches.append(filtered_match)

pprint.pp(filtered_matches)
print(len(filtered_matches))
