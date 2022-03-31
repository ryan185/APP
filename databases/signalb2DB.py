import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['box2project']

mysignalb2collection = mydb["SignalDataB2"]

mysignalb2collection.insert_one({"user_id": 1, "signal": "Stop"})
mysignalb2collection.insert_one({"user_id": 2, "signal": "Stop"})