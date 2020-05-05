from marshmallow import fields

from pynamodb import attributes

from marshmallow_pynamodb import fields as custom_fields

PYNAMODB_TYPE_MAPPING = {
    attributes.NumberAttribute: fields.Number,
    attributes.JSONAttribute: fields.Raw,
    attributes.UnicodeAttribute: fields.String,
    attributes.BooleanAttribute: fields.Boolean,
    attributes.UTCDateTimeAttribute: fields.DateTime,
    attributes.AttributeContainerMeta: custom_fields.PynamoNested,
    attributes.ListAttribute: fields.List,
    attributes.NullAttribute: fields.Raw,
    attributes.UnicodeSetAttribute: custom_fields.UnicodeSet,
    attributes.NumberSetAttribute: custom_fields.NumberSet,
    attributes.BinaryAttribute: custom_fields.BinaryField,
}

try:
    import pynamodb_attributes  # noqa
    from marshmallow_enum import EnumField  # noqa

    PYNAMODB_TYPE_MAPPING.update(
        {
            pynamodb_attributes.uuid.UUIDAttribute: fields.UUID,
            pynamodb_attributes.integer.IntegerAttribute: fields.Integer,
            pynamodb_attributes.unicode_enum.UnicodeEnumAttribute: EnumField,
            pynamodb_attributes.integer_enum.IntegerEnumAttribute: EnumField,
        }
    )
except ImportError:
    pass


def attribute2field(attribute):
    try:
        pynamodb_type = type(attribute)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]
    except KeyError:
        pynamodb_type = type(pynamodb_type)
        field = PYNAMODB_TYPE_MAPPING[pynamodb_type]

    return field
