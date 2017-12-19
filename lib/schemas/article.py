import graphene


class Article(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    content = graphene.String()
