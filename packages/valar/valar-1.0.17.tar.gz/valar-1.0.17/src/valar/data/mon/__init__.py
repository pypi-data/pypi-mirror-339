from bson import ObjectId
from django.db.models import QuerySet
from pymongo.results import InsertOneResult, UpdateResult

from django.conf import settings
import pymongo

from ..query import Query

try:
    MONGO = settings.MONGO_SETTINGS
except AttributeError:
    MONGO = {
        'host': 'localhost',
        'port': 27017,
    }
host, port, username, password = MONGO.get('host'), MONGO.get('port'), MONGO.get('username'), MONGO.get('password')

if username and password:
    uri = f'mongodb://{username}:{password}@{host}:{port}/'
else:
    uri = f'mongodb://{host}:{port}/'
mongo_params = {
    'maxPoolSize': 10,
    'minPoolSize': 0,
    'maxIdleTimeMS': 10000,
    'connectTimeoutMS': 10000,
    'socketTimeoutMS': 10000,
    'serverSelectionTimeoutMS': 10000,
}

def get_mongo_client():
    client = pymongo.MongoClient(uri, **mongo_params)
    client['admin'].command('ping')
    return client



class MongoDao:
    def __init__(self, ref):
        self.ref = ref
        db_name = settings.BASE_APP
        col_name = ref.replace('.', '_')
        self.client = get_mongo_client()
        self.collection = self.client[db_name][col_name]
    def save_one(self, item):
        _id = item.get('id', None)
        _id = None if isinstance(_id, int) else _id
        if _id is None:
            bean:InsertOneResult = self.collection.insert_one(item)
            _id = bean.inserted_id
            self.collection.update_one({'_id': _id}, {'$set': {'sort':str(_id)}})
        else:
            del item['id']
            _id = ObjectId(_id)
            self.collection.update_one({'_id': _id}, {'$set': item})
        return self.collection.find_one({'_id': _id})


    def update_many(self, query, template):
        self.collection.update_many(query.mon_conditions(), {'$set': template})


    def delete_one(self, _id):
        self.collection.delete_one({'_id': ObjectId(_id)})

    def delete_many(self, query):
        self.collection.delete_many(query.mon_conditions())


    def find_one(self, _id):
        return self.collection.find_one({'_id': ObjectId(_id)})

    def find_many(self, query: Query, size=0, page=1) -> [QuerySet, int]:
        skip = (page - 1) * size
        condition = query.mon_conditions()
        total = self.collection.count_documents(condition)
        cursor = self.collection.find(condition).sort(query.orders).skip(skip).limit(size)
        return [cursor, total]


    def meta(self):
        one = self.collection.find_one()
        return one
