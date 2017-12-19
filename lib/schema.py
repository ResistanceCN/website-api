import graphene

from lib.schemas.user import User


class Query(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(default_value="world")
    )
    user_by_id = graphene.Field(
        type=User,
        id=graphene.Int()
    )

    def resolve_hello(self, info, name):
        print(info.context)
        return 'Hello ' + name

    def resolve_user_by_id(self, info, id):
        return User(
            id=id,
            google_id='test_google_id_0000000000',
            name='Test User',
        )


schema = graphene.Schema(query=Query)
