import rom

from rom import UniqueKeyViolation
from flask import abort
from redis import StrictRedis
from redis_lock import Lock
import config
from contextlib import contextmanager
from utils import gen_hash

rom.util.set_connection_settings(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT)

conn = StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT)


class Users(rom.Model):
    email = rom.String(
        required=True,
        unique=True)
    salt = rom.String()
    hash = rom.String()
    phone_number = rom.String(default="")
    balance = rom.Float()






def add_user(email, password):
    salt, hash = gen_hash(password)
    try:
        user = Users(email=email, salt=salt, hash=hash,
                     balance=config.SMS_PRICE *
                     config.FREE_SMS_FOR_NEW_ACCOUNT)
        user.save()
        return user
    except UniqueKeyViolation:
        abort(400, "email already registered")


def get_user(email):
    return Users.get_by(email=email)


@contextmanager
def lock_user(user_email):
    with Lock(conn, 'users/' + user_email, expire=60):
        yield
