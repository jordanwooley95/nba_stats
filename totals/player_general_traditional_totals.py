import requests
from settings import Settings
from models import Totals

settings = Settings()
settings.db.create_tables([Totals], safe=True)

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

season_list = ["2023-24"]

# per_mode = 'Per100Possessions'
per_mode = "Totals"
# per_mode = 'Per36'
# per_mode = 'PerGame'

# for loop to loop over seasons
for season_id in season_list:
    print("Now working on " + season_id + " season")
    # nba stats url to scrape
    player_info_url = (
        "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode="
        + per_mode
        + "&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season="
        + season_id
        + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    )
    # json response
    response = requests.get(url=player_info_url, headers=headers).json()
    # pulling just the data we want
    player_info = response["resultSets"][0]["rowSet"]
    # looping over data to insert into table
    for row in player_info:
        player = Totals(
            season_id=season_id,  # this is key, need this to join and sort by seasons
            player_id=row[0],
            player_name=row[1],
            nickname=row[2],
            team_id=row[3],
            team_abbreviation=row[4],
            age=row[5],
            gp=row[6],
            w=row[7],
            l=row[8],
            w_pct=row[9],
            min=row[10],
            fgm=row[11],
            fga=row[12],
            fg_pct=row[13],
            fg3m=row[14],
            fg3a=row[15],
            fg3_pct=row[16],
            ftm=row[17],
            fta=row[18],
            ft_pct=row[19],
            oreb=row[20],
            dreb=row[21],
            reb=row[22],
            ast=row[23],
            tov=row[24],
            stl=row[25],
            blk=row[26],
            blka=row[27],
            pf=row[28],
            pfd=row[29],
            pts=row[30],
            plus_minus=row[31],
            nba_fantasy_pts=row[32],
            dd2=row[33],
            td3=row[34],
            gp_rank=row[36],
            w_rank=row[37],
            l_rank=row[38],
            w_pct_rank=row[39],
            min_rank=row[40],
            fgm_rank=row[41],
            fga_rank=row[42],
            fg_pct_rank=row[43],
            fg3m_rank=row[44],
            fg3a_rank=row[45],
            fg3_pct_rank=row[46],
            ftm_rank=row[47],
            fta_rank=row[48],
            ft_pct_rank=row[49],
            oreb_rank=row[50],
            dreb_rank=row[51],
            reb_rank=row[52],
            ast_rank=row[53],
            tov_rank=row[54],
            stl_rank=row[55],
            blk_rank=row[56],
            blka_rank=row[57],
            pf_rank=row[58],
            pfd_rank=row[59],
            pts_rank=row[60],
            plus_minus_rank=row[61],
            nba_fantasy_pts_rank=row[62],
            dd2_rank=row[63],
            td3_rank=row[64],
        )

        player.save()
        print("Done")
