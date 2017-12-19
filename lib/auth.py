from flask_graphql import GraphQLView


class Query(GraphQLView):
    def get_context(self, request):
        return request
