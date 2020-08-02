from mongoengine import Document, StringField, ListField, URLField, EmailField


class User(Document):
    name = StringField(required=True, max_length=50)
    phone = StringField(max_length=10)
    email = EmailField(unique=True)
    images = ListField(URLField())
    password = StringField(max_length=20)
    meta = {'allow_inheritance': True}


