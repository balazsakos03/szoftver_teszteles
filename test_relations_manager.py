import pytest
import datetime
from relations_manager import RelationsManager

#fixture
@pytest.fixture
def rm():
    return RelationsManager()

#segedfuggveny
def get_employee_by_name(rm, first_name, last_name):
    for e in rm.get_all_employees():
        if e.first_name == first_name and e.last_name == last_name:
            return e
    return None

#tesztek
# 1. Check if there is a team leader called John Doe whose birthdate is 31.01.1970.
def test_john_doe_is_leader_and_birthdate(rm):
    john = get_employee_by_name(rm, "John", "Doe")
    
    assert john is not None
    assert rm.is_leader(john) is True
    assert john.birth_date == datetime.date(1970, 1, 31)