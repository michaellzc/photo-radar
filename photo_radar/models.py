from peewee import *
from playhouse.sqlite_ext import AutoIncrementField

DATABSE = "photo_radar.db"

db = SqliteDatabase(DATABSE)


def create_tables():
    with db:
        db.create_tables([Camera])


class BaseModel(Model):
    class Meta:
        database = db


class Camera(BaseModel):
    class Meta:
        table_name = "cameras"
        indexes = ((("street", "city", "provience", "country"), True),)

    id = AutoIncrementField()

    street = TextField()
    city = TextField()
    provience = TextField()
    country = TextField()

    lat = FloatField(null=True)
    lon = FloatField(null=True)

    is_red_light_enabled = BooleanField(default=False)
    is_speed_enabled = BooleanField(default=False)
