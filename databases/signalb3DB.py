import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['box2project']

mysignalb3collection = mydb["SignalDataB3"]

mysignalb3collection.insert_one({"user_id": 1, "signal": "Stop"})
mysignalb3collection.insert_one({"user_id": 2, "signal": "Stop"})