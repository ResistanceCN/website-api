import pickle
from flask_graphql import GraphQLView

from lib.stdclass import StdClass
from lib.definition import Faction
from lib.redis import redis


class Context(StdClass):
    def __init__(self, request):
        StdClass.__init__(self)

        self.request = request
        self.user = StdClass(
            id=0,
            faction=Faction.Unspecified,
            is_admin=False,
        )

        self.get_user_info()

    def get_user_info(self):
        try:
            token = self.request.headers.get['Token']
            self.user = pickle.loads(redis.get(token))
        except Exception as e:
            pass


class AuthenticatedView(GraphQLView):
    def get_context(self, request):
        return Context(request)
