from flask import Flask, request
from graphene import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor

import config
from lib.handler.auth import auth
from lib.handler.ql import AuthenticatedView
from lib.schemas.query import Query

if config.DEBUG:
    print('+------------------------------------------------------+')
    print('| WARNING: DEBUG MODE IS ON. TURN IT OFF IN PRODUCTION |')
    print('+------------------------------------------------------+')

app = Flask(__name__)


@app.after_request
def cors(response):
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
        schema=Schema(Query),
        graphiql=config.DEBUG,
        executor=AsyncioExecutor(),
    )
)

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
