import os
import pytest
import sys
from flask import Flask
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WeatherExpress import application




@pytest.fixture(scope='module')
def test_client():
    # Set up a test client that can make requests to the application
    with application.test_client() as client:
        yield client


def test_home_page(test_client):
    # Test that the home page returns a 200 status code
    response = test_client.get('/')
    assert response.status_code == 200


def test_register_page(test_client):
    # Test that the register page returns a 200 status code
    response = test_client.get('/register')
    assert response.status_code == 200


def test_login_page(test_client):
    # Test that the login page returns a 200 status code
    response = test_client.get('/login')
    assert response.status_code == 200


def test_invalid_page(test_client):
    # Test that an invalid page returns a 404 status code
    response = test_client.get('/invalid-page')
    assert response.status_code == 404