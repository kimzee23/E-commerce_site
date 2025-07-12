from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://localhost:27017/")

for db_name in ["ecommerce", "ecommerce_test"]:
    print(f"\n🔍 Inspecting DB: {db_name}")
    db = client[db_name]
    users = list(db.users.find())
    if not users:
        print("  - No users found.")
    else:
        for user in users:
            user["_id"] = str(user["_id"])
            pprint(user)
