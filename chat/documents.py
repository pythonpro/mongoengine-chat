from mongoengine import Document, fields
from mongoengine.django.auth import User
import datetime


class Message(Document):
    author = fields.ReferenceField(User, required=True)
    addressee = fields.ReferenceField(User, required=True)
    text = fields.StringField(required=True, max_length=40)
    created = fields.DateTimeField(required=True,
                                   default=datetime.datetime.now)
    read = fields.BooleanField(required=True, default=False)