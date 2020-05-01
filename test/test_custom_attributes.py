import uuid
from enum import Enum

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
from pynamodb_attributes import IntegerAttribute, UUIDAttribute, UnicodeEnumAttribute

from marshmallow_pynamodb import ModelSchema


class Gender(Enum):
    male = "male"
    female = "female"
    not_informed = "not_informed"


class People(Model):
    class Meta:
        table_name = "people"

    uuid = UUIDAttribute(hash_key=True)
    first_name = UnicodeAttribute()
    last_name = UnicodeAttribute()
    gender = UnicodeEnumAttribute(Gender)
    age = IntegerAttribute()


class PeopleSchema(ModelSchema):
    class Meta:
        model = People


def test_custom_attributes():
    people_schema = PeopleSchema()
    pk = uuid.uuid4()
    payload = {
        "uuid": pk.hex,
        "first_name": "John",
        "last_name": "Doe",
        "gender": Gender.male.value,
        "age": 43,
    }
    people = people_schema.load(payload)
    assert people.gender == Gender.male
    assert people.uuid == pk
