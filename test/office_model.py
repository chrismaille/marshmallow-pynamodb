from enum import Enum
from os import environ

from pynamodb.attributes import (
    BinaryAttribute,
    BooleanAttribute,
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    NumberSetAttribute,
    UTCDateTimeAttribute,
    UnicodeAttribute,
    UnicodeSetAttribute,
)
from pynamodb.models import Model
from pynamodb_attributes import (
    IntegerAttribute,
    IntegerEnumAttribute,
    UUIDAttribute,
    UnicodeEnumAttribute,
)


class PersonGender(Enum):
    male = "M"
    female = "F"


class LocationCategory(Enum):
    one = 1
    two = 2
    three = 3


class Location(MapAttribute):
    latitude = NumberAttribute()
    longitude = NumberAttribute()
    name = UnicodeAttribute()
    category = IntegerEnumAttribute(LocationCategory)
    number_of_seats = NumberAttribute(null=True)


class Person(MapAttribute):
    firstName = UnicodeAttribute()
    lastName = UnicodeAttribute()
    age = IntegerAttribute()
    photo = BinaryAttribute()
    gender = UnicodeEnumAttribute(PersonGender)


class OfficeEmployeeMap(MapAttribute):
    office_employee_id = IntegerAttribute()
    person = Person()
    office_location = Location()
    active = BooleanAttribute()
    start_date = UTCDateTimeAttribute()


class Office(Model):
    class Meta:
        table_name = "OfficeModel"
        host = "http://localhost:{}".format(environ.get("DOCKER_PORT", 8000))

    office_id = UUIDAttribute(hash_key=True)
    address = Location()
    employees = ListAttribute(of=OfficeEmployeeMap)
    departments = UnicodeSetAttribute()
    numbers = NumberSetAttribute()
    security_number = UnicodeAttribute(null=True)
    office_times = ListAttribute()


class Headquarters(Office):
    region = UnicodeAttribute()
