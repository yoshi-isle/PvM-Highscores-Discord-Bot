import json
import pymongo
from pymongo import MongoClient

def GetPersonalBests():
    with open('../config/appsettings.local.json') as settingsJson:
        data = json.load(settingsJson)

    CONNECTION_STRING = data['DbConnectionString']
    CLUSTER_NAME = data['ClusterName']
    DB_NAME = data['DbName']

    cluster = MongoClient(CONNECTION_STRING)

    db = cluster[CLUSTER_NAME]
    collection = db[DB_NAME]

    results = collection.find()

    records = []
    for result in results:
        records.append(result)

    return records