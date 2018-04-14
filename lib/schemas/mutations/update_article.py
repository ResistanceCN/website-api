from datetime import datetime
from bson.objectid import ObjectId
import graphene

from lib.mongo import db
from lib.schemas.types.article import Article


class UpdateArticle(graphene.Mutation):
    class Meta:
        output = Article

    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        content = graphene.String()

    async def mutate(self, info, id, title, content):
        if not info.context.logged_in:
            raise Exception('You must log in to update an article.')

        article = await info.context.loaders.article.load(id)
        if article is None:
            raise Exception('The article does not exist.')

        user = info.context.user
        if not user.is_admin and (user.id != article.author_id or article.published_at is not None):
            raise Exception('Access denied.')

        now = datetime.now()
        db().articles.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'title': title,
                'content': content,
                'updated_at': now,
            },
        })

        article.title = title
        article.content = content
        article.updated_at = now

        return article
