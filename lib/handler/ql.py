from time import time
from bson.objectid import ObjectId
from flask_graphql import GraphQLView

from lib.stdclass import StdClass
from lib.definition import Faction
from lib.mongo import db
from lib.loader.user import UserLoader
from lib.loader.article import ArticleLoader
from lib.loader.user_articles import UserArticlesLoader


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
        self.user = StdClass(
            id=ObjectId('000000000000000000000000'),
            faction=Faction.Unspecified,
            is_admin=False,
        )

        self.get_user_info()

    def get_user_info(self):
        token = self.request.headers.get('Token')

        session = db().sessions.find_one({'token': token})
        if session is None:
            return

        if session.expire < time():
            return db().sessions.delete(session['_id'])

        user = db().users.find_one(session.user_id)
        if user is None:
            return

        self.user = StdClass(
            id=user['_id'],
            faction=user['faction'],
            is_admin=user['is_admin'],
        )


class AuthenticatedView(GraphQLView):
    def get_context(self, request):
        return Context(request)
