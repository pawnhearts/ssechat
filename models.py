import motor.motor_asyncio
from marshmallow import Schema, fields


client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.livechan_db
chat_dbs = db.chat_dbs


class Chat(Schema):
    convo = fields.String()
    convo_id = fields.Number()
    is_convo_op = fields.Boolean(default=False)
    pinned = fields.Number(load_only=True)
    body = fields.String()
    name = fields.String()
    count = fields.Int()
    date = fields.DateTime()
    ip = fields.String(load_only=True)
    identifier = fields.String()
    country = fields.String()
    country_name = fields.String()
    latitude = fields.Number(load_only=True)
    longitude = fields.Number(load_only=True)
    chat = fields.String()
    image = fields.String()
    image_filename = fields.String()
    image_filesize = fields.Number()
    image_width = fields.Number()
    image_height = fields.Number()
    image_transparent = fields.Boolean(load_only=True)
    duration = fields.Number()
    thumb = fields.String()
    trip = fields.String()
    user_agent = fields.String(load_only=True)
    deleted = fields.Boolean(default=False, load_only=True)
