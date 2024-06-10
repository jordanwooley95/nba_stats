import requests
from settings import Settings
from models import BoxScores
from peewee import _transaction
import time

settings = Settings()
settings.db.create_tables([BoxScores], safe=True)

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
    player_info_url = f"https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&ISTRound=&LeagueID=00&PlayerOrTeam=P&Season={season_id}&SeasonType=Playoffs&Sorter=DATE"
    try:
        response = requests.get(url=player_info_url, headers=headers, timeout=10).json()
        print("Fetching Data...")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        break

    player_info = response["resultSets"][0]["rowSet"]

    with _transaction(settings.db):
        for row in player_info:
            defaults = {
                "season_id": season_id,
                "player_id": row[1],
                "player_name": row[2],
                "team_id": row[3],
                "team_abbreviation": row[4],
                "team_name": row[5],
                "game_id": row[6],
                "game_date": row[7],
                "matchup": row[8],
                "wl": row[9],
                "min": row[10],
                "fgm": row[11],
                "fga": row[12],
                "fg_pct": row[13],
                "fg3m": row[14],
                "fg3a": row[15],
                "fg3_pct": row[16],
                "ftm": row[17],
                "fta": row[18],
                "ft_pct": row[19],
                "oreb": row[20],
                "dreb": row[21],
                "reb": row[22],
                "ast": row[23],
                "stl": row[24],
                "blk": row[25],
                "tov": row[26],
                "pf": row[27],
                "pts": row[28],
                "plus_minus": row[29],
                "fantasy_pts": row[30],
            }
            query, created = BoxScores.get_or_create(
                game_id=row[6], player_id=row[1], defaults=defaults
            )
            if not created:
                BoxScores.update(**defaults).where(
                    BoxScores.game_id == row[6], BoxScores.player_id == row[1]
                ).execute()
                print("Data updated")
            else:
                print("Data inserted")

settings.db.commit()
