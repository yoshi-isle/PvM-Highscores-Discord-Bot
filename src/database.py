import json

from pymongo import MongoClient
from bson.objectid import ObjectId


class Database:
    def __init__(self, settings_path="../config/appsettings.local.json"):
        with open(settings_path) as settings_json:
            settings = json.load(settings_json)

        self.connection_string = settings["DbConnectionString"]
        self.db_name = settings["DbName"]
        self.cluster_name = settings["PersonalBestsClusterName"]

        self._connect()

    def _connect(self):
        self.cluster = MongoClient(self.connection_string)
        self.db = self.cluster[self.db_name]
        self.collection = self.db[self.cluster_name]

    def get_personal_bests(self):
        return [result for result in self.collection.find()]

    def insert_personal_best_submission(self, submission):
        insert_data = {
            "boss": submission.boss,
            "pb": submission.pb,
            "discord_cdn_url": submission.discord_cdn_url,
            "date_achieved": submission.date_achieved,
            "osrs_username": submission.osrs_username,
            "discord_username": submission.discord_username,
            "approved": submission.approved,
        }
        return self.collection.insert_one(insert_data).inserted_id

    def get_personal_best_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})
