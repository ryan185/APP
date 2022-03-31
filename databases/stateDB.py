import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

mystatecollection = mydb["StateData"]

# mystatecollection.insert_one({"user_id": 1, "state": "1"})
# mystatecollection.insert_one({"user_id": 2, "state": "1"})
# mystatecollection.insert_one({"user_id": 3, "state": "1"})
mystatecollection.insert_one({"user_id": 4, "state": "1"})