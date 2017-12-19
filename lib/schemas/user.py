import graphene

import lib.schemas.article


class User(graphene.ObjectType):
    id = graphene.Int()
    google_id = graphene.String()
    name = graphene.String()
    articles = graphene.List(of_type=lib.schemas.article.Article)

    def resolve_articles(self, info):
        return [
            lib.schemas.article.Article(id=1, title='Test Article 1'),
            lib.schemas.article.Article(id=2, title='Test Article 2')
        ]
