import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['box2project']

mysignalb1collection = mydb["SignalDataB1"]

mysignalb1collection.insert_one({"user_id": 1, "signal": "Stop"})
mysignalb1collection.insert_one({"user_id": 2, "signal": "Stop"})