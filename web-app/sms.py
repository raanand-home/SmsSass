import os
import requests

SMS_SERVICE_URL = os.environ.get('SMS_SERVICE_URL',
                                 'https://rest.nexmo.com/sms/json')

API_KEY = os.environ['SMS_API_KEY']
API_SECRET = os.environ['SMS_API_SECRET']
DEFAULT_SENDER = 'Sms Sender'


def send(to, text, sender=DEFAULT_SENDER):
    requests.post(SMS_SERVICE_URL,
                  json={
                      'api_key': API_KEY,
                      'api_secret': API_SECRET,
                      'from': sender,
                      'text': text,
                      'to': to,
                  })
