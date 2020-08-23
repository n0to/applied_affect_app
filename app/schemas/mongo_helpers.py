from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.base.datastructures import LazyReference


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")
        return str(v)


class LazyReferenceStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, LazyReference):
            return str(v.id)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Invalid LazyReferenceStr")
