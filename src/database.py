import json
from pymongo import MongoClient
import data.personal_best as personal_best

def get_personal_bests():
    with open("../config/appsettings.local.json") as settings_json:
        settings = json.load(settings_json)

    CONNECTION_STRING = settings["DbConnectionString"]
    CLUSTER_NAME = settings["ClusterName"]
    DB_NAME = settings["DbName"]

    cluster = MongoClient(CONNECTION_STRING)
    db = cluster[CLUSTER_NAME]
    collection = db[DB_NAME]

    results = collection.find()
    records = [result for result in results]
    return records

def insert_pending_submission(submission):
    with open("../config/appsettings.local.json") as settings_json:
        settings = json.load(settings_json)

    CONNECTION_STRING = settings["DbConnectionString"]
    DB_NAME = settings["DbName"]
    CLUSTER_NAME = settings["PbEntryClusterName"]

    cluster = MongoClient(CONNECTION_STRING)
    db = cluster[DB_NAME]
    collection = db[CLUSTER_NAME]

    mydict = { "boss": submission.boss, "pb": submission.pb }
    id = collection.insert_one(mydict).inserted_id
    return id