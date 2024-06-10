from peewee import *
from BaseModel import BaseModel


class BoxScores(BaseModel):
    season_id = CharField(null=True)
    player_id = IntegerField(null=True)
    player_name = CharField(null=True)
    team_id = IntegerField(null=True)
    team_abbreviation = CharField(null=True)
    team_name = CharField(null=True)
    game_id = CharField(null=True)
    game_date = CharField(null=True)
    matchup = CharField(null=True)
    wl = CharField(null=True)
    min = IntegerField(null=True)
    fgm = IntegerField(null=True)
    fga = IntegerField(null=True)
    fg_pct = FloatField(null=True)
    fg3m = IntegerField(null=True)
    fg3a = IntegerField(null=True)
    fg3_pct = FloatField(null=True)
    ftm = IntegerField(null=True)
    fta = IntegerField(null=True)
    ft_pct = FloatField(null=True)
    oreb = IntegerField(null=True)
    dreb = IntegerField(null=True)
    reb = IntegerField(null=True)
    ast = IntegerField(null=True)
    stl = IntegerField(null=True)
    blk = IntegerField(null=True)
    tov = IntegerField(null=True)
    pf = IntegerField(null=True)
    pts = IntegerField(null=True)
    plus_minus = IntegerField(null=True)
    fantasy_pts = FloatField(null=True)
    # data is coming from nba_sql.db

    class Meta:
        table_name = "boxscores"
