import logging
from flask import Flask, request
from graphene import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor

import config
from lib.handlers.auth import auth
from lib.handlers.ql import AuthenticatedView
from lib.schemas.query import Query
from lib.schemas.mutation import Mutation

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

if config.DEBUG:
    origin_handler = app.handle_http_exception

    def log_handler(e):
        print(e)
        return origin_handler(e)

    app.handle_http_exception = log_handler


@app.after_request
def access_control(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = request.headers.get('Access-Control-Request-Methods')
    response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers')
    return response


app.add_url_rule('/auth', endpoint='auth', view_func=auth)
app.add_url_rule(
    '/graphql',
    endpoint='graphql',
    view_func=AuthenticatedView.as_view(
        name='graphql',
        schema=Schema(query=Query, mutation=Mutation),
        graphiql=config.DEBUG,
        executor=AsyncioExecutor(),
    )
)

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
