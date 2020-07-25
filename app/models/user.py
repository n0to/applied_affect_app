from mongoengine import Document, StringField, ListField, URLField


class User(Document):
    name = StringField(required=True)
    phone = StringField()
    email = StringField(required=True, unique=True)
    images = ListField(URLField())
    meta = {'abstract': True}


