import pymongo

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

mystopkanripart2dbcollection = mydb["StopKanriPart2DB"]

mystopkanripart2dbcollection.insert_one({"user_id": 1, "value": True})