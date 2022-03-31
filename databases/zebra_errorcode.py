import pymongo

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

myzebraalertcollection = mydb["ZEBRA"]

myzebraalertcollection.insert_one({"user_id": 1, "Error_code": "1"})