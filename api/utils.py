import serpy


class SerpyWithContext(serpy.Serializer):
    def __init__(self, *args, **kwargs):
        super(SerpyWithContext, self).__init__(*args, **kwargs)
        if "context" in kwargs:
            self.context = kwargs["context"]
