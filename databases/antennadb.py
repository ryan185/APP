import pymongo
import pandas as pd

myclient = pymongo.MongoClient("localhost", 27017)
mydb2 = myclient['box2project']

myantennab1collection = mydb2["AntennaDataB1"]
myantennab2collection = mydb2["AntennaDataB2"]
myantennab3collection = mydb2["AntennaDataB3"]
myantennab4collection = mydb2["AntennaDataB4"]

myantennab1collection.insert_one({"user_id": 1,"antennaA": "1", "antennaB": "2"})
myantennab2collection.insert_one({"user_id": 1,"antennaA": "3", "antennaB": "4"})
myantennab3collection.insert_one({"user_id": 1,"antennaA": "5", "antennaB": "6"})
myantennab4collection.insert_one({"user_id": 1,"antennaA": "7", "antennaB": "8"})