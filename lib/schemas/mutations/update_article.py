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

    async def mutate(self, info, id, title=None, content=None):
        if not info.context.logged_in:
            raise Exception('You must log in to update an article.')

        article = await info.context.loaders.article.load(id)
        if article is None:
            raise Exception('The article does not exist.')

        me = info.context.user
        if me.id != article.author_id or article.status != ArticleStatus.DRAFT:
            raise Exception('Access denied.')

        now = datetime.now()
        fields_set = {'updated_at': now}
        article.updated_at = now

        if title is not None:
            if len(title) == 0:
                raise Exception('The title must not be empty.')
            fields_set['title'] = title
            article.title = title

        if content is not None:
            if len(content) == 0:
                raise Exception('The content must not be empty.')
            fields_set['content'] = content
            article.content = content

        db().articles.update_one({'_id': ObjectId(id)}, {'$set': fields_set})

        return article
