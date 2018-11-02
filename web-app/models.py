from api import api
from flask_restplus import fields

new_user = api.model('NewUser', {
    'email': fields.String(description='user email', required=True),
    'password': fields.String(description='password', required=True),
})

user = api.model('User', {
    'email': fields.String(description='User id', required=True),
    'balance': fields.Float(description='Current User balance', required=True)
})

login_info = api.model('LoginInfo', {
    'email': fields.String(description='user email', required=True),
    'password': fields.String(description='password', required=True),
})

auth_info = api.model(
    'AuthInfo', {
        'token': fields.String(
            description='Oldrefresh token', required=True),
    })

phone_number = api.model('PhoneNumber', {
    'phone_number': fields.String(
        description='Phone number', required=True),
})

user_phone_verification_request = api.model(
    'UserPhoneVerificationRequest', {
        'request_token':
            fields.String(
                description='request phone verification token', required=True)
    })

user_phone_verification_verify = api.model(
    'UserPhoneVerificationVerify', {
        'request_token':
            fields.String(description='request token', required=True),
        'verification_code':
            fields.String(
                description='verification code received from the user',
                required=True),
    })


sms_send = api.model(
    'SmsSendRequest', {
        'phone_number':
            fields.String(
                description='Phone number to send to', required=True),
        'text':
            fields.String(
                description='Text message',
                required=True),
        'sender': fields.String(
            description='Text message sender',
            required=True),
    })
