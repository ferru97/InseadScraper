class Author:

    def __init__(self):
        DEFAULT_VALUE = "--"

        id = DEFAULT_VALUE
        link = DEFAULT_VALUE
        name = DEFAULT_VALUE
        job = DEFAULT_VALUE
        locations = DEFAULT_VALUE
        beats = DEFAULT_VALUE
        seenIn = DEFAULT_VALUE
        description = DEFAULT_VALUE
        email = DEFAULT_VALUE
        telephone = DEFAULT_VALUE
        website = DEFAULT_VALUE
        twitterFollower = DEFAULT_VALUE
        twitterTweets = DEFAULT_VALUE
        facebook = DEFAULT_VALUE
        twitter = DEFAULT_VALUE
        linkedin = DEFAULT_VALUE
        instagram = DEFAULT_VALUE
        threads = DEFAULT_VALUE

    def getCsvRecord(self):
        return self.__dict__
