import logging

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from constants.cluster_names import MongodbConstants
from settings import get_environment_variable


class Database:
    def __init__(self):
        self.mongo_uri = get_environment_variable("MONGODB_CONNECTION_STRING")
        self.logger = logging.getLogger("discord")
        self._connect()

    def _connect(self):
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi("1"))
        try:
            self.client.admin.command("ping")
            self.logger.info("mongo connected")
        except Exception as e:
            self.logger.critical(f"mongo did not connect: {e}")

        self.db = self.client[MongodbConstants.cluster_name]
        self.pb_collection = self.db[MongodbConstants.collection_personal_bests_name]
        self.signup_collection = self.db[MongodbConstants.collection_signups_name]
        self.mgmt_collection = self.db[MongodbConstants.collection_management_name]
        self.summerland_collection = self.db[
            MongodbConstants.collection_summerland_name
        ]

    def _disconnect(self):
        self.client.close()

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

    async def new_signup(self, submission):
        insert_data = {
            "discord name": submission.discord_name,
            "osrs name": submission.osrs_username,
            "team mates": submission.team_mates,
            "paid": False,
            "paid proof cdn": "",
        }
        return self.signup_collection.insert_one(insert_data).inserted_id

    async def add_persistent_message_id(
        self, message_key, message_id, optional_state=None
    ):
        return self.mgmt_collection.insert_one(
            {
                "message_key": message_key,
                "message id": message_id,
                "optional_state": optional_state,
            }
        ).inserted_id

    async def get_personal_best_by_id(self, id):
        return self.pb_collection.find_one({"_id": ObjectId(id)})

    async def set_personal_best_approved(self, id, url):
        update_data = {"$set": {"approved": True, "discord_cdn_url": url}}
        return self.pb_collection.update_one({"_id": ObjectId(id)}, update_data)

    async def update_personal_best(self, id, key, value):
        update_data = {"$set": {key: value}}
        return self.pb_collection.update_one({"_id": ObjectId(id)}, update_data)

    # Summerland Bingo

    async def get_team_info(self, channel_id):
        return self.summerland_collection.find_one({"channel_id": str(channel_id)})

    async def get_all_teams(self):
        return self.summerland_collection.find()

    async def update_team_tile(self, channel_id, key, value):
        update_data = {"$set": {key: value}}
        return self.summerland_collection.update_one(
            {"channel_id": channel_id}, update_data
        )
