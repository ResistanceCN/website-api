from bson.objectid import ObjectId
import graphene

from lib.mongo import db
from lib.schemas.types.join_info import JoinInfo, JoinStatus


class UpdateJoinInfo(graphene.Mutation):
    class Meta:
        output = JoinInfo

    class Arguments:
        user_id = graphene.ID(required=True)
        status = JoinStatus()
        comment = graphene.String()

    async def mutate(self, info, user_id, status=None, comment=None):
        print(user_id)

        fields_set = {}
        if status is not None:
            fields_set['join_info.status'] = status
        if comment is not None:
            fields_set['join_info.comment'] = comment

        db().users.update_one({'_id': ObjectId(user_id)}, {
            '$set': fields_set,
        })

        user = db().users.find_one({'_id': ObjectId(user_id)})

        return JoinInfo.from_dict({
            **user['join_info'],
            'user_id': user_id,
        })
