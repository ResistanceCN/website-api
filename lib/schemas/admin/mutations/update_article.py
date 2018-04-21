from datetime import datetime
from bson.objectid import ObjectId
import graphene

from lib.mongo import db
from lib.schemas.types.article import Article, ArticleStatus


class UpdateArticle(graphene.Mutation):
    class Meta:
        output = Article

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()
        status = ArticleStatus()

    async def mutate(self, info, id, title=None, content=None, status=None):
        article = await info.context.loaders.article.load(id)
        if article is None:
            raise Exception('The article does not exist.')

        now = datetime.now()
        fields_set = {'updated_at': now}
        article.updated_at = now

        if title is not None:
            fields_set['title'] = title
            article.title = title
        if content is not None:
            fields_set['content'] = content
            article.content = content
        if status is not None:
            fields_set['status'] = status
            article.status = status
            if status == ArticleStatus.PUBLISHED:
                fields_set['published_at'] = now
                article.published_at = now

        db().articles.update_one({'_id': ObjectId(id)}, {
            '$set': fields_set,
        })

        return article
