from flask_restplus import Resource
from api import api
from models import sms_send
from dal import get_user, lock_user
from utils import verify_user
import sms
import flask
import config


@api.route('/sms')
class PhoneVerificationVerification(Resource):
    @api.doc(responses={400: 'Invalid Argument'},
             body=sms_send,
             description="Send SMS"
             )
    @verify_user
    def post(self, user):
        with lock_user(user['email']):
            user_obj = get_user(email=user['email'])
            if user_obj.phone_number is None or \
                    user_obj.phone_number == "":
                flask.abort(400, "User phone number is not Verified")
            if user_obj.balance - config.SMS_PRICE < 0:
                flask.abort(400, "Insufficient balance")
            sms.send(to=api.payload['phone_number'],
                     text=api.payload['text'],
                     sender=api.payload['sender'])
            user_obj.balance = user_obj.balance - config.SMS_PRICE
            user_obj.save()
