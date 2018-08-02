from bson.objectid import ObjectId
import graphene

from lib.mongo import db

class EmptyJoinInfo(graphene.Mutation):
    class Meta:
        output = graphene.Boolean

    class Arguments:
        id = graphene.ID(required=True)

    async def mutate(self, info, id):
        join_info = {
            'agent_name': '',
            'telegram': '',
            'regions': [],
            'other': '',
            'updated_at': None,
        }

        db().user.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'join_info': join_info
            }
        })