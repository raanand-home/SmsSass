import requests
import pytest
from helpers import (get_random_email,
                     create_user,
                     login_user,
                     verify_user,
                     query_last_message,
                     MOCK_PREFIX,
                     send_sms)


def send_sms_to_mock(phone, text):
    response = requests.post(MOCK_PREFIX + '/sms/json', json={
        'api_key': 'api_key',
        'api_secret': 'api_secret',
        'from': 'from',
        'text': text,
        'to': phone,
    })
    response.raise_for_status()
    return response.json()


def test_send_sms():
    email = get_random_email()
    create_user(email, 'pass')
    token = login_user(email, 'pass')
    verify_user(token)
    send_sms(token, '+123', 'text', 'god')
    last_message = query_last_message('+123')
    assert last_message['text'] == 'text'
    assert last_message['from'] == 'god'


def test_send_sms_without_verify_throws_exception():
    email = get_random_email()
    create_user(email, 'pass')
    token = login_user(email, 'pass')
    with pytest.raises(requests.HTTPError):
        send_sms(token, '+123', 'text', 'god')


def test_balance_sms_send_balance_depleted():
    email = get_random_email()
    create_user(email, 'pass')
    token = login_user(email, 'pass')
    verify_user(token)
    for dummy in xrange(5):
        send_sms(token, '+123', 'text', 'god')

    with pytest.raises(requests.HTTPError):
        send_sms(token, '+123', 'text', 'god')


def test_mock():
    send_sms_to_mock('123', 'text')
    assert query_last_message('123')['text'] == 'text'
