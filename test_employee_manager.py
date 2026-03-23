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


# 2. Check an employee’s salary who is a team leader and his team consists of 3 members. 
# She was hired on 10.10.2008 and has a base salary of 2000$. 
# Validate if the returned value is 3600$ (2000$ + 10 X 100$ + 3 X 200$).
@patch('employee_manager.datetime.date', MockDate)
def test_leader_salary_with_3_members(em, rm):
    #vezeto letrehozasa
    leader = Employee(
        id=100, first_name="Boss", last_name="Lady", base_salary=2000,
        birth_date=datetime.date(1980, 1, 1), 
        hire_date=datetime.date(2008, 10, 10)
    )
    
    #nem adatbazisbol van ezert beavatkozas a relationsmanagerbe
    #rafogjuk hogy o egy vezeto es harom embere van
    rm.is_leader = MagicMock(return_value=True)
    rm.get_team_members = MagicMock(return_value=[101, 102, 103]) #harom fos csapat
    
    salary = em.calculate_salary(leader)
    
    assert salary == 3600


# 3. Make sure that when you calculate the salary and send an email notification, 
# the respective email sender service is used with the correct information.
@patch('builtins.print') #print fuggveny mockolasa mivel nem kuld emailt
@patch('employee_manager.datetime.date', MockDate)
def test_salary_notification(mock_print, em, rm):
    leader = Employee(
        id=100, first_name="Boss", last_name="Lady", base_salary=2000,
        birth_date=datetime.date(1980, 1, 1), 
        hire_date=datetime.date(2008, 10, 10)
    )
    
    rm.is_leader = MagicMock(return_value=True)
    rm.get_team_members = MagicMock(return_value=[101, 102, 103])
    
    #fizetes szamolasa es "email" kuldese
    em.calculate_salary_and_send_email(leader)
    
    #print meghivas ellenorzes
    mock_print.assert_called_once()
    
    #megfelelo szoveggel lett e meghivva
    expected_message = "Boss Lady your salary: 3600 has been transferred to you."
    mock_print.assert_called_with(expected_message)