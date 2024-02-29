class Tweet:

    def __init__(self):
        DEFAULT_VALUE = "--"

        authorId = DEFAULT_VALUE
        date = DEFAULT_VALUE
        link = DEFAULT_VALUE
        text = DEFAULT_VALUE
        
    def getCsvRecord(self):
        return self.__dict__
