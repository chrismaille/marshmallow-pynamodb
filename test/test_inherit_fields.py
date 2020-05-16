import uuid
from pynamodb_attributes import UnicodeEnumAttribute, UUIDAttribute
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
from marshmallow_pynamodb import ModelSchema
from enum import Enum


class MyStatus(Enum):
    CREATED = "CREATED"


class BaseDocument(Model):
    uuid = UUIDAttribute(default=uuid.uuid4)


class MyDocument(BaseDocument):
    status = UnicodeEnumAttribute(MyStatus, default=MyStatus.CREATED)
    content = UnicodeAttribute()


class MyDocumentSchema(ModelSchema):
    class Meta:
        model = MyDocument
        inherit_field_models = True


def test_inherit_fields():
    instance = MyDocumentSchema().load({"content": "foo"})
    assert isinstance(instance.uuid, uuid.UUID)
    assert instance.status == MyStatus.CREATED
    assert instance.content == "foo"
