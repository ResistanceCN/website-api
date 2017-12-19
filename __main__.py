from flask import Flask

import config
from lib.schema import schema
from lib.auth import Query

if config.DEBUG:
    print('+------------------------------------------------------+')
    print('| WARNING: DEBUG MODE IS ON. TURN IT OFF IN PRODUCTION |')
    print('+------------------------------------------------------+')

app = Flask(__name__)
app.add_url_rule(
    '/graphql',
    view_func=Query.as_view(
        name='graphql',
        schema=schema,
        graphiql=config.DEBUG
    )
)
app.run(host=config.LISTEN, port=config.PORT, debug=config.DEBUG)
