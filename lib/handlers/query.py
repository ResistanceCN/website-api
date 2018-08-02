from dataclasses import dataclass
from time import time
import logging
from bson.objectid import ObjectId
from flask import request
from flask_graphql import GraphQLView
from graphql.error.base import GraphQLError
from graphene import Schema
from graphql.execution.executors.asyncio import AsyncioExecutor

import config
from lib.definition import Faction
from lib.mongo import db
from lib.loaders.user import UserLoader
from lib.loaders.article import ArticleLoader
from lib.loaders.user_articles import UserArticlesLoader
from lib.schemas.query import Query
from lib.schemas.mutation import Mutation
from lib.schemas.admin.query import AdminQuery
from lib.schemas.admin.mutation import AdminMutation


class Context:
    @dataclass
    class Loaders:
        user: UserLoader
        article: ArticleLoader
        user_articles: UserArticlesLoader

    @dataclass
    class User:
        id: ObjectId = ObjectId('000000000000000000000000')
        faction: Faction = Faction.Unspecified
        is_admin: bool = False

    @dataclass
    class NewUser:
        google_id: str
        email: str
        avatar: str

    def __init__(self, req):
        self.request = req

        # DataLoaders
        self.loaders = Context.Loaders(
            user=UserLoader(),
            article=ArticleLoader(),
            user_articles=UserArticlesLoader(),
        )

        # Empty user
        self.logged_in = False
        self.user = Context.User()

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
            self.new_user = Context.NewUser(
                google_id=session['google_id'],
                email=session['email'],
                avatar=session['avatar'],
            )
            return

        user = db().users.find_one(session['user_id'])
        if user is None:
            return

        self.user = Context.User(
            id=user['_id'],
            faction=user['faction'],
            is_admin=user['is_admin'],
        )
        self.logged_in = True


class AuthenticatedView(GraphQLView):
    def __init__(self, **kwargs):
        GraphQLView.__init__(self, **kwargs)
        self.context = Context(request)

    def get_context(self):
        return self.context

    @staticmethod
    def format_error(error):
        if isinstance(error, GraphQLError):
            logging.error('Exception on %s [%s]' % (
                request.path,
                request.method
            ), exc_info=error)

        return GraphQLView.format_error(error)


class AdminView(AuthenticatedView):
    def dispatch_request(self):
        if self.context.user is None or not self.context.user.is_admin:
            raise Exception("Access denied!")

        return AuthenticatedView.dispatch_request(self)


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
