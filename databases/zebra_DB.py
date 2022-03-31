import pymongo

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']

myapidbcollection = mydb["APIData"]

myapidbcollection.insert_one({"user_id": 1, "apidata": True})
# myapidbcollection.update_one({"user_id": 1},{'$set':{"apidata": True}})