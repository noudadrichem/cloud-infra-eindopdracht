class UserService:
    def __init__(self, db):
        self.db = db

    def create(self, user):
        userId = self.db.get().users.insert(user)
        user = self.getById(userId)
        print('user', user)
        return {**user, '_id': str(user['_id'])}

    def update(self, userId, body):
        user = self.db.get().users.update_one({'_id': body['_id']}, body)
        print('user', user)
        return {**user, '_id': str(user['_id'])}

    def getById(self, userId):
        return self.db.get().users.find_one({ '_id': userId})

    def getByGoogleId(self, googleId):
        return self.db.get().users.find_one({ 'googleId': googleId})
