from peewee import *
from BaseModel import BaseModel


class PlayerInfo(BaseModel):
    person_id = IntegerField(null=True)
    player_last_name = CharField(null=True)
    player_first_name = CharField(null=True)
    jersey_number = IntegerField(null=True)
    position = CharField(null=True)
    height = CharField(null=True)
    weight = IntegerField(null=True)
    college = CharField(null=True)
    country = CharField(null=True)
    draft_year = IntegerField(null=True)
    draft_round = IntegerField(null=True)
    draft_number = IntegerField(null=True)

    class Meta:
        table_name = "player_info"
