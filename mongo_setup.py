# mongo_setup.py

from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["rna_seq_data"]
    return db
