import datetime

from mongoengine import Document, StringField, ListField, URLField, EmailField, DateTimeField


class User(Document):
    name = StringField(required=True, max_length=50)
    phone = StringField(max_length=10)
    email = EmailField(unique=True)
    images = ListField(URLField())
    datetime_modified = DateTimeField(default=datetime.datetime.now)
    hashed_password = StringField(max_length=20)
    meta = {'allow_inheritance': True}


