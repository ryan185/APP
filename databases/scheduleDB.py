import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

mysavedaycollection = mydb["SaveDayData"]
mysavehourcollection = mydb["SaveHourData"]
mysaveminutecollection = mydb["SaveMinuteData"]

mykanripart2savehourcollection = mydb["KanriPart2SaveHourData"]
mykanripart2saveminutecollection = mydb["KanriPart2SaveMinuteData"]


mysavedaycollection.insert_one({"user_id": 1, "day": "29"})
mysavehourcollection.insert_one({"user_id": 1, "hour": "8"})
mysaveminutecollection.insert_one({"user_id": 1, "minute": "00"})

mykanripart2savehourcollection.insert_one({"user_id": 1, "hour": "8"})
mykanripart2saveminutecollection.insert_one({"user_id": 1, "minute": "00"})