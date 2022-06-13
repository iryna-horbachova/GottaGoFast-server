import pymongo


client = pymongo.MongoClient()
database = client['ggf_locations']
collection = database["geotags"]


class GeoStorageManager:

    @staticmethod
    def insert_many(entries):
        collection.insert_many(entries)

    @staticmethod
    def insert_one(entry):
        collection.insert_one(entry)

    @staticmethod
    def find_latest_user_location(user_id):
        query = {"user_id": user_id}
        location = collection.find_one(query, sort=[('timestamp', -1)])

        print("******* LOCATIONS")
        print(location)

        return location
