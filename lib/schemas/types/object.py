import graphene


class ObjectType(graphene.ObjectType):
    def __init__(self, *args, **kwargs):
        graphene.ObjectType.__init__(self, *args, **kwargs)
        self._hidden_fields = {}

    def hide_field(self, field: str):
        value = getattr(self, field)
        setattr(self, field, None)
        self._hidden_fields[field] = str

    def get_field(self, field: str):
        value = getattr(self, field)
        if value is not None:
            return value

        try:
            return self._hidden_fields[field]
        except KeyError:
            return None
