# coding=utf-8
from pymongo import MongoClient

class MYMongoclient():
    def __init__(self):
        client = MongoClient()
        self.collection = client["job"]["zhilian"]

    def save_item(self,item):
        if isinstance(item,dict):
            self.collection.insert(item)


_mongo_client = MYMongoclient()
save_item = _mongo_client.save_item
