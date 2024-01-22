import json

from pymongo import MongoClient

from hall_of_fame.constants.personal_best import PersonalBest


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

    mydict = {"boss": submission.boss, "pb": submission.pb}
    id = collection.insert_one(mydict).inserted_id
    return id
