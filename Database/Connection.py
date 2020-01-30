from pymongo import MongoClient


class ConnectionModel:
    @staticmethod
    def connect(collection_name):
        connection_url = MongoClient('localhost', 27017)
        return connection_url["demo"][collection_name]

