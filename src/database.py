from bson.objectid import ObjectId
from pymongo import MongoClient
from settings import get_environment_variable
from constants.cluster_names import DiscordDatabase


class Database:
    def __init__(self):
        self.connection_string = get_environment_variable("MONGODB_CONNECTION_STRING")
        self._connect()

    def _connect(self):
        self.cluster = MongoClient(self.connection_string)
        self.db = self.cluster[DiscordDatabase.name]
        self.pb_collection = self.db[DiscordDatabase.personal_bests]

    async def get_personal_bests(self):
        return [result for result in self.pb_collection.find({"approved": True})]

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
        return self.pb_collection.insert_one(insert_data).inserted_id

    async def get_personal_best_by_id(self, id):
        return self.pb_collection.find_one({"_id": ObjectId(id)})

    async def update_personal_best_approval(self, id, approved):
        update_data = {"$set": {"approved": approved}}
        return self.pb_collection.update_one({"_id": ObjectId(id)}, update_data)
