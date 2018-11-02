import requests
import uuid
import re


HOST = 'localhost:5000'
MOCK_PREFIX = 'http://localhost:5002'


def get_path(path):
    return 'http://' + HOST + '/' + path


def create_user(email, password):
    response = requests.post(
        get_path('user'), json={'email': email, 'password': password})
    response.raise_for_status()
    return response.json()


def get_random_email():
    return "{}@gmail.com".format(uuid.uuid4())


def login_user(email, password):
    response = requests.post(
        get_path('login'), json={'email': email, 'password': password})
    response.raise_for_status()
    return response.json()['token']


def _get_headers(token):
    return {'Authorization': 'Bearer {}'.format(token)}


def refresh_token(token):
    response = requests.post(get_path('login/refresh'),
                             headers=_get_headers(token=token))
    response.raise_for_status()
    return response.json()['token']


def user_phone_verification_request(token, phone_number):
    response = requests.post(get_path('user/phone_verification/request'),
                             headers=_get_headers(token=token),
                             json={'phone_number': phone_number})
    response.raise_for_status()
    return response.json()


def user_phone_verification_verify(token, request_token, verification_code):
    response = requests.post(get_path('user/phone_verification/verify'),
                             headers=_get_headers(token=token),
                             json={'request_token': request_token,
                                   'verification_code': verification_code
                                   })
    response.raise_for_status()


def query_last_message(phone):
    response = requests.get(MOCK_PREFIX + '/sms/{}'.format(phone))
    response.raise_for_status()
    return response.json()


def send_sms(token, number, text, sender):
    response = requests.post(get_path('sms'), json={
        'phone_number': number,
        'text': text,
        'sender': sender
    }, headers=_get_headers(token=token))
    response.raise_for_status()
    return response.json()


def verify_user(token):
    request = user_phone_verification_request(
        token, '+33241')
    message_text = query_last_message('+33241')['text']
    code = re.findall(
        r'Verification Code:(\d\d\d-\d\d\d)', message_text)[0]
    user_phone_verification_verify(
        token=token,
        request_token=request['request_token'],
        verification_code=code)


def get_user(token):
    response = requests.get(
        get_path('user'), headers=_get_headers(token=token))
    response.raise_for_status()
    return response.json()
