import pytest
import datetime
from unittest.mock import patch, MagicMock
from employee import Employee
from relations_manager import RelationsManager
from employee_manager import EmployeeManager

#fixtures
@pytest.fixture
def rm():
    return RelationsManager()

@pytest.fixture
def em(rm):
    return EmployeeManager(rm)

#segedosztaly az ido fagyasztasahoz
class MockDate(datetime.date): #"kamu" (mock) datum osztaly ami mindig 2018 at ad vissza a today() hivasra
    @classmethod
    def today(cls):
        return cls(2018, 1, 1)

#tesztek

# 1. Check an employee’s salary who is not a team leader whose hire date is 10.10.1998 and his base salary is 1000$. 
# Make sure the returned value is 3000$ (1000$ + 20 X 100$).
@patch('employee_manager.datetime.date', MockDate) #kicsereli a date osztalyt
def test_regular_employee_salary(em):
    #sajat dolgozo letrehozasa
    emp = Employee(
        id=99, first_name="Regular", last_name="Joe", base_salary=1000,
        birth_date=datetime.date(1980, 1, 1), 
        hire_date=datetime.date(1998, 10, 10)
    )
    
    #fizetes szamolasa
    salary = em.calculate_salary(emp)
    
    assert salary == 3000