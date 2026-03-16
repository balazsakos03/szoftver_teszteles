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

# 2. Check if John Doe’s team members are Myrta Torkelson and Jettie Lynch
def test_john_doe_team_members(rm):
    john = get_employee_by_name(rm, "John", "Doe")
    member_ids = rm.get_team_members(john) #[2, 3]
    
    #id alapu kereses, majd a neveket listaba
    members = [e for e in rm.get_all_employees() if e.id in member_ids]
    member_names = [f"{e.first_name} {e.last_name}" for e in members]
    
    assert "Myrta Torkelson" in member_names
    assert "Jettie Lynch" in member_names

# 3. Make sure that Tomas Andre is not John Doe’s team member.
def test_tomas_andre_not_in_johns_team(rm):
    john = get_employee_by_name(rm, "John", "Doe")
    member_ids = rm.get_team_members(john)
    
    members = [e for e in rm.get_all_employees() if e.id in member_ids]
    member_names = [f"{e.first_name} {e.last_name}" for e in members]
    
    assert "Tomas Andre" not in member_names