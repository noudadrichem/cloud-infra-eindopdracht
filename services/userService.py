from bson.objectid import ObjectId

class UserService:
    def __init__(self, db):
        self.db = db

    def create(self, user):
        userId = self.db.get().users.insert(user)
        user = self.getById(userId)
        print('user', user)

    def update(self, userId, body):
        self.db.get().users.update_one({'_id': userId }, {'$set': { **body } })
        user = self.getById(userId)
        print('user', user)
        return {**user, '_id': str(user['_id'])}

    def getById(self, userId):
        user = self.db.get().users.find_one({ '_id': ObjectId(userId)})
        print('get by id... = ', user)
        return user

    def getByGoogleId(self, googleId):
        return self.db.get().users.find_one({ 'googleId': googleId})

    def getByToken(self, token):
        user = self.db.get().users.find_one({ 'token': token})
        print('get by token... = ', user)
        return user
