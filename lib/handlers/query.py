from time import time
import logging
from bson.objectid import ObjectId
from flask import request
from flask_graphql import GraphQLView
from graphql.execution import ExecutionResult
from graphene import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor

import config
from lib.stdclass import StdClass
from lib.definition import Faction
from lib.mongo import db
from lib.loaders.user import UserLoader
from lib.loaders.article import ArticleLoader
from lib.loaders.user_articles import UserArticlesLoader
from lib.schemas.query import Query
from lib.schemas.mutation import Mutation
from lib.schemas.admin.query import AdminQuery
from lib.schemas.admin.mutation import AdminMutation


class Context(StdClass):
    def __init__(self, request):
        StdClass.__init__(self)

        self.request = request

        # DataLoaders
        self.loaders = StdClass(
            user=UserLoader(),
            article=ArticleLoader(),
            user_articles=UserArticlesLoader(),
        )

        # Empty user
        self.logged_in = False
        self.user = StdClass(
            id=ObjectId('000000000000000000000000'),
            faction=Faction.Unspecified,
            is_admin=False,
        )

        self.new_user = None

        self.get_user_info()

    def get_user_info(self):
        token = self.request.headers.get('Token')

        session = db().sessions.find_one({'token': token})
        if session is None:
            return

        if session['expire'] < time():
            return db().sessions.delete_one({'_id': session['_id']})

        if session.get('new_user'):
            self.new_user = StdClass(
                google_id=session['google_id'],
                email=session['email'],
            )
            return

        user = db().users.find_one(session['user_id'])
        if user is None:
            return

        self.user = StdClass(
            id=user['_id'],
            faction=user['faction'],
            is_admin=user['is_admin'],
        )
        self.logged_in = True


class AuthenticatedView(GraphQLView):
    def __init__(self, **kwargs):
        GraphQLView.__init__(self, **kwargs)
        self.context = Context(request)

    def execute_graphql_request(self, data, query, variables, operation_name, show_graphiql=False):
        result = GraphQLView.execute_graphql_request(self, data, query, variables, operation_name, show_graphiql)

        if isinstance(result, ExecutionResult) and result.invalid:
            for error in result.errors:
                logging.error('Exception on %s [%s]' % (
                    request.path,
                    request.method
                ), exc_info=error)

        return result


class AdminView(AuthenticatedView):
    def execute(self, *args, **kwargs):
        if self.context.user is None or not self.context.user.is_admin:
            raise Exception("Access denied!")

        return AuthenticatedView.execute(self, *args, **kwargs)


api_view = AuthenticatedView.as_view(
    name='api',
    schema=Schema(query=Query, mutation=Mutation),
    graphiql=config.DEBUG,
    executor=AsyncioExecutor(),
)

admin_api_view = AdminView.as_view(
    name='admin_api',
    schema=Schema(query=AdminQuery, mutation=AdminMutation),
    graphiql=config.DEBUG,
    executor=AsyncioExecutor(),
)
