
from dal import add_user
import rom.util
import config
import logging

from api import app
import routes

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
