from bson.objectid import ObjectId
import graphene

from lib.mongo import db


class DeleteArticle(graphene.Mutation):
    class Meta:
        output = graphene.Int

    class Arguments:
        id = graphene.ID(required=True)

    async def mutate(self, info, id):
        result = db().articles.delete_one({'_id': ObjectId(id)})
        return result.deleted_count
