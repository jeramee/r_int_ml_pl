# mongo_setup.py

from pymongo import MongoClient

def connect_mongo(db_name="r_int_ml_pl_data"):
    """
    Establishes a connection to MongoDB and returns the specified database.
    
    Parameters:
    - db_name (str): Name of the MongoDB database. Default is "r_int_ml_pl_data".

    Returns:
    - db (Database): MongoDB database object.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    return db

def get_collections(db):
    """
    Returns references to the main collections in the database.
    
    Parameters:
    - db (Database): MongoDB database object.

    Returns:
    - dict: Dictionary containing references to the collections.
    """
    collections = {
        "deseq2_results": db["deseq2_results"],
        "samples": db["samples"],
        "projects": db["projects"],  # Optional collection for projects
    }
    return collections
