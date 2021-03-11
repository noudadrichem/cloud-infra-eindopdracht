import pymongo

class DatabaseService:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin:Wachtwoord12345@cim.4iwoq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client.cim

    def get(self):
        return self.db
