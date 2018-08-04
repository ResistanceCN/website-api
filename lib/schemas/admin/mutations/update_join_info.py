from bson.objectid import ObjectId
import graphene

from lib.mongo import db


class UpdateJoinInfo(graphene.Mutation):
    class Meta:
        output = graphene.Boolean

    class Arguments:
        id = graphene.ID(required=True)

    async def mutate(self, info, id):
        # @TODO
        pass
