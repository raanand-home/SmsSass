from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_restplus import fields


app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Mock SMS API',
          description='Nexmo Mock',
          )

sms_info = api.model('Send SMS', {
    'api_key': fields.String(description='api key', required=True),
    'api_secret': fields.String(description='api secret', required=True),
    'from': fields.String(description='From text', required=True),
    'text': fields.String(description='SMS text', required=True),
    'to': fields.String(description='phone number', required=True),
})

data = {}


@api.route('/sms/json')
class SendSms(Resource):
    @api.doc(responses={404: 'Email Not found or password not match'},
             body=sms_info)
    def post(self):
        global data
        data[api.payload['to']] = api.payload


@api.route('/sms/<phone_number>')
class QuerySms(Resource):
    @api.doc(responses={404: 'Email Not found or password not match'},
             body=sms_info)
    def get(self, phone_number):
        global data
        return data[phone_number]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
