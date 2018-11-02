import requests
import pytest
from helpers import (create_user,
                     get_random_email,
                     login_user,
                     refresh_token, get_user)
from requests import HTTPError
HOST = 'localhost:5000'


def test_register():
    email = get_random_email()
    new_user = create_user(email, 'pass')
    assert new_user['email'] == email


def test_register_user_twice():
    email = get_random_email()
    create_user(email, 'pass')
    with pytest.raises(requests.HTTPError):
        create_user(email, 'pass')


def test_login():
    email = get_random_email()
    create_user(email, 'pass')
    token = login_user(email, 'pass')
    token = refresh_token(token)


def test_token_guard():
    email = get_random_email()
    create_user(email, 'pass')
    token = login_user(email, 'pass')
    with pytest.raises(HTTPError):
        token = refresh_token(token + '1')


def test_login_with_bad_password():
    email = get_random_email()
    create_user(email, 'pass')
    with pytest.raises(HTTPError):
        login_user(email, 'wrong_pass')


def test_get_current():
    email = get_random_email()
    create_user(email, 'pass')
    token = login_user(email, 'pass')
    user = get_user(token=token)
    assert user['email'] == email
    assert user['balance'] == 2.5
