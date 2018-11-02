import rom
import os
from hashlib import sha256
from rom import UniqueKeyViolation
from flask import abort
from redis import StrictRedis
from redis_lock import Lock
import config
from contextlib import contextmanager
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


PASSES = 32768


def gen_hash(password, salt=None):
    salt = salt or os.urandom(16)
    comp = salt + password.encode('utf-8')
    out = sha256(comp).digest()
    for i in xrange(PASSES - 1):
        out = sha256(out + comp).digest()
    return salt, out


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
