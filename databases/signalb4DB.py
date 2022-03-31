import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['box2project']

mysignalb4collection = mydb["SignalDataB4"]

mysignalb4collection.insert_one({"user_id": 1, "signal": "Stop"})
mysignalb4collection.insert_one({"user_id": 2, "signal": "Stop"})