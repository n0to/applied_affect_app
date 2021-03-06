from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    ListField,
    URLField,
    EmailField,
    DateTimeField)


class User(Document):
    name = StringField(required=True, max_length=50)
    phone = StringField(max_length=10)
    email = EmailField(unique=True)
    images = ListField(URLField())
    datetime_modified = DateTimeField(default=datetime.now)
    hashed_password = StringField(max_length=100)
    meta = {'allow_inheritance': True}


class Admin(User):
    pass

