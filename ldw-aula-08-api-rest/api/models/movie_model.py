from api import mongo

class Movie():
    def __init__(self, title, description, year, duration):
        self.title = title
        self.description = description
        self.year = year
        self.duration = duration