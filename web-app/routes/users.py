import datetime
import random
from flask_restplus import Resource
from api import api
from models import (new_user,
                    user,
                    user_phone_verification_request,
                    user_phone_verification_verify,
                    phone_number)
from dal import add_user, get_user
from utils import (verify_user,
                   encode_data,
                   decode_data_and_verify,
                   gen_hash
                   )
import sms
import base64

random.seed()


@api.route('/user')
class User(Resource):
    @api.doc(responses={400: 'Invalid Argument'},
             body=new_user, description="Register New User")
    @api.marshal_with(user)
    def post(self):
        user = add_user(email=api.payload['email'],
                        password=api.payload['password'])
        return {'email': user.email,
                'balance': user.balance
                }

    @api.doc(description="Get current user information")
    @api.marshal_with(user)
    @verify_user
    def get(self, user):
        user = get_user(user['email'])
        return {'email': user.email,
                'balance': user.balance
                }


@api.route('/user/phone_verification/request')
class PhoneVerificationRequest(Resource):
    @api.doc(responses={400: 'Invalid Argument'},
             body=phone_number,
             description='Request the system to validate user phone number')
    @api.marshal_with(user_phone_verification_request)
    @verify_user
    def post(self, user):
        verification_code = str(random.randint(100, 999)) + \
            '-' + str(random.randint(100, 999))
        sms.send(api.payload['phone_number'],
                 "Verification Code:" + verification_code)
        salt, hash = gen_hash(verification_code)
        request_token = encode_data(
            {'code': {
                'sha256': base64.urlsafe_b64encode(hash),
                'salt': base64.urlsafe_b64encode(salt)},
             'phone_number': api.payload['phone_number']},
            datetime.timedelta(minutes=5))
        return {'request_token': request_token}


@api.route('/user/phone_verification/verify')
class PhoneVerificationVerification(Resource):
    @api.doc(responses={400: 'Invalid Argument'},
             body=user_phone_verification_verify,
             description='''
    This method take a valid phone verification request token
    and the code that was sent to the phone and verify they are a match
    ''')
    @verify_user
    def post(self, user):
        encoded_data = decode_data_and_verify(api.payload['request_token'])
        hash = gen_hash(api.payload['verification_code'],
                        base64.urlsafe_b64decode(
                            str(encoded_data['code']['salt'])))[1]
        if base64.urlsafe_b64decode(
                str(encoded_data['code']['sha256'])) != hash:
            return "verification code doesn't match", 400
        user_obj = get_user(email=user['email'])
        user_obj.phone_number = encoded_data['phone_number'].encode('utf-8')
        user_obj.save()
