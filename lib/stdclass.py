class StdClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        d = self.__dict__
        for key, value in d.items():
            if isinstance(value, StdClass):
                d[key] = value.to_dict()
        return d
