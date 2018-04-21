import logging
from flask import Flask, request

import config
from lib.handlers.auth import auth
from lib.handlers.query import api_view, admin_api_view

if config.DEBUG:
    print('+------------------------------------------------------+')
    print('| WARNING: DEBUG MODE IS ON. TURN IT OFF IN PRODUCTION |')
    print('+------------------------------------------------------+')

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.after_request
def access_control(response):
    headers = request.headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = headers.get('Access-Control-Request-Methods')
    response.headers['Access-Control-Allow-Headers'] = headers.get('Access-Control-Request-Headers')
    return response


app.add_url_rule('/auth', endpoint='auth', view_func=auth)
app.add_url_rule('/api', endpoint='api', view_func=api_view)
app.add_url_rule('/admin_api', endpoint='admin_api', view_func=admin_api_view)

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
