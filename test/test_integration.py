import json
from copy import deepcopy
from datetime import datetime
from uuid import UUID

import pytest
from marshmallow import ValidationError

from test.office_model import Location, Office, OfficeEmployeeMap, Person
from test.office_schema import OfficeSchema


def test_attributes(data_dumps):
    data = OfficeSchema().load(data_dumps)

    assert getattr(OfficeSchema, "_declared_fields")["office_id"].required is True
    assert isinstance(data, Office)

    assert data.attribute_values["office_id"] == UUID(
        "18e430b0-a968-4c22-8b82-9735e94ca058"
    )

    assert isinstance(data.attribute_values["address"], Location)
    assert isinstance(data.attribute_values["departments"], list)
    assert isinstance(data.attribute_values["numbers"], list)
    assert isinstance(data.attribute_values["employees"], list)
    assert isinstance(data.attribute_values["employees"][0], OfficeEmployeeMap)
    assert isinstance(data.attribute_values["employees"][0]["person"], Person)
    assert isinstance(
        data.attribute_values["employees"][0]["office_location"], Location
    )


def test_validation(data_dumps):
    bad_attrs = deepcopy(data_dumps)
    bad_attrs.pop("office_id")

    with pytest.raises(ValidationError) as errors:
        OfficeSchema().load(bad_attrs)

    assert errors.value.messages, {"office_id": ["Not a valid number."]}


@pytest.mark.freeze_time("2020-04-21")
def test_dump(data_attrs, data_dumps, freezer):
    model = Office(**data_attrs)

    data = OfficeSchema().dump(model)

    data["departments"] = sorted(data["departments"])
    data["employees"][0]["start_date"] = data_dumps["employees"][0]["start_date"]
    data["employees"][1]["start_date"] = data_dumps["employees"][1]["start_date"]

    assert data == data_dumps


@pytest.mark.freeze_time("2020-04-21")
def test_dump_between_pynamo_and_model_schema(data_attrs, data_dumps, freezer):
    model_from_pynamo = Office(**data_attrs)

    payload = json.dumps(data_dumps)
    model_from_schema: Office = OfficeSchema().loads(payload)

    model_from_pynamo.departments = sorted(model_from_pynamo.departments)
    model_from_schema.departments = sorted(model_from_schema.departments)

    model_from_pynamo.employees[0]["start_date"] = datetime(2020, 4, 21, 12, 0, 0)
    model_from_pynamo.employees[1]["start_date"] = datetime(2020, 4, 21, 12, 0, 0)
    model_from_schema.employees[0]["start_date"] = datetime(2020, 4, 21, 12, 0, 0)
    model_from_schema.employees[1]["start_date"] = datetime(2020, 4, 21, 12, 0, 0)

    dump_from_pynamo = OfficeSchema().dumps(model_from_pynamo)
    dump_from_schema = OfficeSchema().dumps(model_from_schema)

    assert dump_from_pynamo == dump_from_schema
