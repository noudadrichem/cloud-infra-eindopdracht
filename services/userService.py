from bson.objectid import ObjectId
# ? https://console.cloud.google.com/apis/credentials?project=cim-eindopracht
class UserService:
    def __init__(self, db):
        self.db = db

    def create(self, user):
        userId = self.db.get().users.insert(user)
        user = self.getById(userId)

    def update(self, userId, body):
        self.db.get().users.update_one({'_id': userId }, {'$set': { **body } })
        user = self.getById(userId)
        return {**user, '_id': str(user['_id'])}

    def getById(self, userId):
        user = self.db.get().users.find_one({ '_id': ObjectId(userId)})
        return user

    def getByGoogleId(self, googleId):
        return self.db.get().users.find_one({ 'googleId': googleId})

    def getByToken(self, token):
        user = self.db.get().users.find_one({ 'token': token})
        return user
