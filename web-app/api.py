
from flask import Flask
from flask_restplus import Api
from Crypto.PublicKey import RSA
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app, version='0,1', title='SMS Sender',
          description='SMS Sender API',
          )

app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['JWT_ALGORITHM'] = 'RS256'
jwt_key = RSA.generate(2048)
app.config['JWT_PRIVATE_KEY'] = jwt_key.exportKey('PEM')
app.config['JWT_PUBLIC_KEY'] = jwt_key.publickey().exportKey('PEM')
jwt_manager = JWTManager(app)
