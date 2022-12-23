class Table(dict):
    __path__: str
    __name__: str


    def __init__(self, *arg, **kwargs):
        super(Table, self).__init__(*arg, **kwargs)


    def save(self) -> None:
        pass
