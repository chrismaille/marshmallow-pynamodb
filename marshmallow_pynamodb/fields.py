import warnings
from base64 import b64decode, b64encode

from marshmallow import fields
from marshmallow.exceptions import ValidationError


class Binary64Field:
    def __new__(cls, *args, **kwargs):
        """Binary64 Field deprecated."""
        warnings.warn(
            "This field is deprecated. "
            "It will removed on next version. "
            "Please, use BinaryField(base64=True) instead.",
            DeprecationWarning,
        )
        return BinaryField(base64=True, *args, **kwargs)


class BinaryField(fields.Field):
    def __init__(self, base64: bool = True, encoding: str = "utf-8", **kwargs):
        """Bytestring field.

        :param base64: True or False, setting this will encode/decode the binary in base64. Default: True
        :param encoding: Set byte encoding - Default: utf-8
        :param kwargs: The same keyword arguments that :class:`Field` receives.
        """

        super().__init__(**kwargs)
        self.base64 = base64
        self.encoding = encoding

    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError("Invalid input type.")

    def _deserialize(self, value, attr, data, **kwargs):
        if not value:
            return None
        if self.base64:
            return b64decode(value.encode(self.encoding))
        else:
            return value.encode(self.encoding)

    def _serialize(self, value, attr, data, **kwargs):
        if not value:
            return None
        if self.base64:
            return b64encode(value).decode(self.encoding)
        else:
            return value.decode(self.encoding)


class PynamoNested(fields.Nested):
    def _serialize(self, nested_obj, attr, obj):
        if not isinstance(nested_obj, dict):
            nested_obj = nested_obj.attribute_values
        return super(PynamoNested, self)._serialize(nested_obj, attr, obj)


class PynamoSet(fields.List):
    def __init__(self, cls_or_instance, **kwargs):
        self.strict_unique = kwargs.pop("strict_unique", True)
        super(PynamoSet, self).__init__(cls_or_instance, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if self.strict_unique:
            unfiltered_value = super(PynamoSet, self)._deserialize(
                value, attr, data, **kwargs
            )
            duplicates = dict()
            unique_list = set()

            for element in unfiltered_value:
                if element in unique_list:
                    duplicates[element] = ["Duplicate element"]
                else:
                    unique_list.add(element)

            if duplicates:
                raise ValidationError(duplicates)
        else:
            unique_list = set(
                super(PynamoSet, self)._deserialize(value, attr, data, **kwargs)
            )

        return unique_list

    def _serialize(self, value, attr, obj, **kwargs):
        return super(PynamoSet, self)._serialize(value, attr, obj, **kwargs)


class NumberSet(PynamoSet):
    def __init__(self, **kwargs):
        super(NumberSet, self).__init__(fields.Number, **kwargs)


class UnicodeSet(PynamoSet):
    def __init__(self, **kwargs):
        super(UnicodeSet, self).__init__(fields.String, **kwargs)
