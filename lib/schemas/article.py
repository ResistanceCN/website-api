import graphene

import lib.schemas.user
import lib.loader.user


class Article(graphene.ObjectType):
    id = graphene.ID()
    author_id = graphene.Int()
    author = graphene.Field(lambda: lib.schemas.user.User)
    tags = graphene.List(graphene.String)
    title = graphene.String()
    content = graphene.String()
    created_at = graphene.String()
    updated_at = graphene.String()
    published_at = graphene.String()

    async def resolve_author(self, info):
        author = await info.context.loaders.user.load(self.author_id)
        lib.loader.user.filter_user_fields(author, info.context)
        return author
