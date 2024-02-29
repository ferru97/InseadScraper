class Article:

    def __init__(self):
        DEFAULT_VALUE = "--"

        authorId = DEFAULT_VALUE
        title = DEFAULT_VALUE
        link = DEFAULT_VALUE
        date = DEFAULT_VALUE
        authors = DEFAULT_VALUE
        description = DEFAULT_VALUE

    def getCsvRecord(self):
        return self.__dict__
