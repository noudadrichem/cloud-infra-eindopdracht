class RecordService:
    def __init__(self, db):
        self.db = db

    def create(self, record):
        recordId = self.db.get().records.insert(record)
        record = self.getById(recordId)
        print('record', record)
        return {**record, '_id': str(record['_id'])}
    
    def update(self, recordId, body):
        record = self.db.get().records.update({'_id': body['_id']}, body)
        print('record', record)
        return {**record, '_id': str(record['_id'])}
    
    # def delete(self, recordId):
    #     return self.db.get().records.delete({ '_id': record['_id'] })

    def getById(self, recordId):
        return self.db.get().records.find_one({ '_id': recordId})

    def get(self):
        return self.db.get().records.find()
