import pymongo


class GeoStorageManager(object):
    client = pymongo.MongoClient()
    database = client['ggf_locations']
    collection = database["geotags"]

    @staticmethod
    def insert_many(self, entries):
        self.collection.insert_many(entries)

    @staticmethod
    def insert_one(self, entry):
        self.collection.insert_one(entry)

    @staticmethod
    def find_latest_user_location(self, user_id):
        query = {"user_id": user_id}
        locations = self.collection.find(query).sort("timestamp", -1)
        if not locations:
            return None
        return locations[0]
