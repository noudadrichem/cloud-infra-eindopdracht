import pymongo

class DatabaseService:
    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://admin:Wachtwoord12345@cim.4iwoq.mongodb.net/cim?authSource=admin&retryWrites=true&w=majority",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client.cim

    def get(self):
        return self.db
