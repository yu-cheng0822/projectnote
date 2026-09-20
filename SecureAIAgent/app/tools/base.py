class Tool:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, **kwargs):
        raise NotImplementedError