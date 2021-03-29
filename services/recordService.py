from bson.objectid import ObjectId

class RecordService:
    def __init__(self, db):
        self.db = db

    def create(self, record):
        recordId = self.db.get().records.insert(record)
        record = self.getById(recordId)
        print('record', record)
        return {**record, '_id': str(record['_id'])}
    
    def update(self, body):
        self.db.get().records.update({'_id': ObjectId(body['id'])}, body)
        record = self.getById(body['id'])
        print('record', record)
        return {**record, '_id': str(record['_id'])}
    
    # def delete(self, recordId):
    #     return self.db.get().records.delete({ '_id': record['_id'] })

    def getById(self, recordId):
        return self.db.get().records.find_one({ '_id': ObjectId(recordId)})

    def get(self):
        return self.db.get().records.find()

    def getByUserId(self, userId):
        query = { 'user': userId }
        records = self.db.get().records.find(query)
        tmp = []
        for x in records: # TODO  beetje een zooitje
            tmp.append({**x, '_id': str(x['_id'])})
        return tmp
