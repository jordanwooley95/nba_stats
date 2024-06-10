import requests
from settings import Settings
from models import PlayerInfo
from peewee import _transaction
import time

settings = Settings()
settings.db.create_tables([PlayerInfo], safe=True)

headers = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-token": "true",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "x-nba-stats-origin": "stats",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Referer": "https://stats.nba.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}

season_list = [
    "2023-24",
]

for season_id in season_list:
    player_info_url = f"https://stats.nba.com/stats/playerindex?College=&Country=&DraftPick=&DraftRound=&DraftYear=&Height=&Historical=1&LeagueID=00&Season={season_id}&SeasonType=Regular%20Season&TeamID=0&Weight="
    try:
        response = requests.get(url=player_info_url, headers=headers, timeout=10).json()
        print("Fetching Data...")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        break

    player_info = response["resultSets"][0]["rowSet"]

    with _transaction(settings.db):
        for row in player_info:
            person_id = row[0]  
            defaults = {
                "person_id": person_id,
                "player_last_name": row[1],
                "player_first_name": row[2],
                "jersey_number": row[10],
                "position": row[11],
                "height": row[12],
                "weight": row[13],
                "college": row[14],
                "country": row[15],
                "draft_year": row[16],
                "draft_round": row[17],
                "draft_number": row[18],
            }
            query, created = PlayerInfo.get_or_create(
                person_id=row[0], defaults=defaults
            )
            if not created:
                PlayerInfo.update(**defaults).where(
                    PlayerInfo.person_id == row[0]
                ).execute()
                print("Updating data...")
            else:
                print("Data inserted")

settings.db.commit()