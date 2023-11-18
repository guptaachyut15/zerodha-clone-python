from pymongo import MongoClient
from datetime import datetime

order_book = {
    "GOOGLE": {
        "Sell": [{"user_id": "6558ad16c3b8b4ef90ca9f98", "quantity": 2, "price": 1200}],
        "Buy": [],
    },
    "TWITTER": {"Sell": [], "Buy": []},
}


class MongoDB:
    client = None

    def __init__(self) -> None:
        if not self.client:
            self.client = MongoClient("mongodb://localhost:27017/")
        self.db_kite = self.client["kite-clone"]

    def upsert_document(self, collection, data):
        data["datetime"] = datetime.now()
        doc = self.db_kite[collection].insert_one(data)
        return doc.inserted_id

    def get_document(self, collection, filter={}):
        return self.db_kite[collection].find_one(filter)

    def update_document(self, collection, filter, data):
        return self.db_kite[collection].update_one(filter=filter, update={"$set": data})
