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
