from marshmallow import fields

from marshmallow_pynamodb import ModelSchema
from test.office_model import Office


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
