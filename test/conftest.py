import uuid
from datetime import datetime

import pytest

from test.office_model import LocationCategory, Office, PersonGender


@pytest.fixture(autouse=True)
def create_table():
    if not Office.exists():
        Office.create_table(read_capacity_units=1, write_capacity_units=1)

    yield
    Office.delete_table()


@pytest.fixture
def data_dumps():
    return {
        "address": {
            "latitude": 6.98454,
            "longitude": 172.38832,
            "name": "some_location",
            "category": 3,
        },
        "departments": sorted(["engineering", "dev-ops", "UI/UX", "sales"]),
        "employees": [
            {
                "active": True,
                "office_employee_id": 123,
                "office_location": {
                    "latitude": -24.0853,
                    "longitude": 144.8766,
                    "name": "other_location",
                    "category": 1,
                },
                "person": {
                    "age": 45,
                    "firstName": "John",
                    "lastName": "Smith",
                    "photo": "cGhvdG9fam9obl9zbWl0aA==",
                    "gender": "M",
                },
                "start_date": datetime.utcnow().isoformat(),
            },
            {
                "active": True,
                "office_employee_id": 456,
                "office_location": {
                    "latitude": -20.57989,
                    "longitude": 92.30463,
                    "name": "yal",
                    "category": 2,
                },
                "person": {
                    "age": 33,
                    "firstName": "Jane",
                    "lastName": "Doe",
                    "photo": "cGhvdG9famFuZV9kb2U=",
                    "gender": "F",
                },
                "start_date": datetime.utcnow().isoformat(),
            },
        ],
        "numbers": [1, 2, 3, 4, 5, 6],
        "office_id": "18e430b0-a968-4c22-8b82-9735e94ca058",
        "office_times": ["standard", 8, 17],
    }


@pytest.fixture
def data_attrs():
    return {
        "address": {
            "latitude": 6.98454,
            "longitude": 172.38832,
            "name": "some_location",
            "category": LocationCategory.three,
        },
        "employees": [
            {
                "office_employee_id": 123,
                "active": True,
                "start_date": datetime.utcnow(),
                "person": {
                    "firstName": "John",
                    "lastName": "Smith",
                    "age": 45,
                    "photo": b"photo_john_smith",
                    "gender": PersonGender.male,
                },
                "office_location": {
                    "latitude": -24.0853,
                    "longitude": 144.87660,
                    "name": "other_location",
                    "category": LocationCategory.one,
                },
            },
            {
                "office_employee_id": 456,
                "active": True,
                "start_date": datetime.utcnow(),
                "person": {
                    "firstName": "Jane",
                    "lastName": "Doe",
                    "age": 33,
                    "photo": b"photo_jane_doe",
                    "gender": PersonGender.female,
                },
                "office_location": {
                    "latitude": -20.57989,
                    "longitude": 92.30463,
                    "name": "yal",
                    "category": LocationCategory.two,
                },
            },
        ],
        "departments": set(sorted(["engineering", "dev-ops", "UI/UX", "sales"])),
        "numbers": [1, 2, 3, 4, 5, 6],
        "office_id": uuid.UUID("18e430b0-a968-4c22-8b82-9735e94ca058"),
        "office_times": ["standard", 8, 17],
    }
