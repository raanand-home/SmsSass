
import jwt
import datetime
from functools import wraps
import flask
import dateutil.parser
from flask_jwt_extended import (
    verify_jwt_refresh_token_in_request,
    get_jwt_identity
)
from api import app


def encode_data(data, timeout):
    valid_until = (
        datetime.datetime.utcnow() + timeout).isoformat()
    encoded = jwt.encode({
        'valid_until':
        valid_until, 'data': data},
        app.config['JWT_PRIVATE_KEY'],
        algorithm=app.config['JWT_ALGORITHM'])
    return encoded


def decode_data_and_verify(encoded_data):
    decoded = jwt.decode(
        encoded_data.encode('utf-8'), app.config['JWT_PUBLIC_KEY'],
        algorithms=app.config['JWT_ALGORITHM'])
    if dateutil.parser.parse(
            decoded['valid_until']) < datetime.datetime.utcnow():
        raise jwt.exceptions.ExpiredSignatureError()
    return decoded['data']


def verify_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_refresh_token_in_request()
        except:
            flask.abort(401)
        if kwargs is None:
            kwargs = {}
        kwargs['user'] = get_jwt_identity()
        return fn(*args, **kwargs)
    return wrapper
