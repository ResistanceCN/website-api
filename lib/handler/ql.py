from bson.objectid import ObjectId
from flask_graphql import GraphQLView

from lib.stdclass import StdClass
from lib.definition import Faction
from lib.mongo import db
from lib.loader.loaders import Loaders


class Context(StdClass):
    def __init__(self, request):
        StdClass.__init__(self)

        self.request = request
        self.loaders = Loaders

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

        user = db().users.find_one(session.user_id)
        if user is None:
            return

        self.user = StdClass(
            id=user['_id'],
            faction=user['faction'],
            is_admin=user['is_admin']
        )


class AuthenticatedView(GraphQLView):
    def get_context(self, request):
        return Context(request)
