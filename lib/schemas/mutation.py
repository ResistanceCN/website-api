import graphene

from .mutations.create_profile import CreateProfile


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
