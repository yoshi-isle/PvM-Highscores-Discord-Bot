from bson.objectid import ObjectId
from pymongo import MongoClient


class Database:
    def __init__(self, settings: dict):
        self.connection_string = settings["DbConnectionString"]
        self.db_name = settings["DbName"]
        self.cluster_name = settings["PersonalBestsClusterName"]

        self._connect()

    def _connect(self):
        self.cluster = MongoClient(self.connection_string)
        self.db = self.cluster[self.db_name]
        self.collection = self.db[self.cluster_name]

    async def get_personal_bests(self):
        return [result for result in self.collection.find()]

    async def insert_personal_best_submission(self, submission):
        insert_data = {
            "boss": submission.boss,
            "pb": submission.pb.strftime("%H:%M:%S.%f"),
            "discord_cdn_url": submission.discord_cdn_url,
            "date_achieved": submission.date_achieved,
            "osrs_username": submission.osrs_username,
            "discord_username": submission.discord_username,
            "approved": submission.approved,
        }
        return self.collection.insert_one(insert_data).inserted_id

    async def get_personal_best_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    async def update_personal_best_approval(self, id, approved):
        update_data = {"$set": {"approved": approved}}
        return self.collection.update_one({"_id": ObjectId(id)}, update_data)
