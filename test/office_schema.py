from marshmallow import fields

from marshmallow_pynamodb import ModelSchema
from test.office_model import Office, Headquarters


class OfficeSchema(ModelSchema):
    """Office Schema for PynamoDB Office Model.

    We are overriding PynamoDB
    NumberSetAttribute and UnicodeSetAttribute fields
    to maintain list order

    """

    numbers = fields.List(fields.Integer)
    departments = fields.List(fields.String)

    class Meta:
        """Schema Model Meta Class."""

        model = Office


class HQSchema(OfficeSchema):
    """Model Schema with parent Schemas field Introspection.

    Fields are introspected using
    parent marshmallow ModelSchemas. (ex.: OfficeSchema Schema)

    """
    class Meta:
        model = Headquarters


class HeadquartersSchema(ModelSchema):
    """Model Schema with parent Models field Introspection.

    Fields are introspected using
    parent PynamoDB Models. (ex.: Office Model)

    """
    class Meta:
        model = Headquarters
        inherit_field_models = True
