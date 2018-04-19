from datetime import datetime
import graphene

from lib.mongo import db
from lib.schemas.types.article import Article


class CreateArticle(graphene.Mutation):
    class Meta:
        output = Article

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    async def mutate(self, info, title, content):
        if not info.context.logged_in:
            raise Exception('You must log in to create an article.')

        user = info.context.user
        if not user.is_admin:
            count = db().articles.find({
                'author_id': user.id,
                'published_at': None
            }).count()
            if count >= 3:
                raise Exception('You have already submitted 3 drafts. Try completing and publishing them.')

        if len(title) == 0:
            raise Exception('The title must not be empty.')
        if len(content) == 0:
            raise Exception('The content must not be empty.')

        now = datetime.now()
        result = db().articles.insert_one({
            'author_id': user.id,
            'title': title,
            'content': content,
            'created_at': now,
            'updated_at': now,
        })

        article = Article(
            id=result.inserted_id,
            author_id=user.id,
            title=title,
            content=content,
            tags=[],
            created_at=now,
            updated_at=now,
            published_at=None,
        )

        return article
