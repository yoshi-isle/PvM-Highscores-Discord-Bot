import json

from pymongo import MongoClient
import data.personal_best as personal_best
from bson.objectid import ObjectId

def get_personal_bests():
    with open("../config/appsettings.local.json") as settings_json:
        settings = json.load(settings_json)

    CONNECTION_STRING = settings["DbConnectionString"]
    DB_NAME = settings["DbName"]
    CLUSTER_NAME = settings["PersonalBestsClusterName"]

    cluster = MongoClient(CONNECTION_STRING)
    db = cluster[DB_NAME]
    collection = db[CLUSTER_NAME]

    results = collection.find()
    records = [result for result in results]
    return records

def insert_pending_submission(submission):
    with open("../config/appsettings.local.json") as settings_json:
        settings = json.load(settings_json)

    CONNECTION_STRING = settings["DbConnectionString"]
    DB_NAME = settings["DbName"]
    CLUSTER_NAME = settings["PersonalBestsClusterName"]

    cluster = MongoClient(CONNECTION_STRING)
    db = cluster[DB_NAME]
    collection = db[CLUSTER_NAME]

    insert_data = { "boss": submission.boss, "pb": submission.pb, "osrs_username": submission.osrs_username }
    id = collection.insert_one(insert_data).inserted_id
    return id

def get_personal_best_by_id(id):
    with open("../config/appsettings.local.json") as settings_json:
        settings = json.load(settings_json)

    CONNECTION_STRING = settings["DbConnectionString"]
    DB_NAME = settings["DbName"]
    CLUSTER_NAME = settings["PersonalBestsClusterName"]

    cluster = MongoClient(CONNECTION_STRING)
    db = cluster[DB_NAME]
    collection = db[CLUSTER_NAME]
    
    return collection.find_one({'_id': ObjectId(id) })