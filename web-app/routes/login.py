from api import api
from flask_restplus import Resource
from models import login_info, auth_info
import flask
from flask_jwt_extended import create_refresh_token
from utils import verify_user, gen_hash
from dal import get_user


@api.route('/login')
class Login(Resource):
    @api.doc(responses={404: 'Email Not found or password not match'},
             body=login_info,
             description="Login User returns refresh token for future login")
    @api.marshal_with(auth_info)
    def post(self):
        user = get_user(api.payload['email'])
        if gen_hash(
                api.payload['password'],
                user.salt)[1] != user.hash:
            flask.abort(403)
        return {'token':
                create_refresh_token(
                    {'email': user.email}
                )}


@api.route('/login/refresh')
class RefreshToken(Resource):
    @api.doc(description="Refresh token to keep session alive")
    @api.marshal_with(auth_info)
    @verify_user
    def post(self, user):
        return {'token': create_refresh_token(user)}
