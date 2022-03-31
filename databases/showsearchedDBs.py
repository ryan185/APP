import pandas as pd
import pymongo
from datetime import datetime, timedelta,date
import json

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myrecordpgshowdatedbcollection = mydb["RecordShowDateDB"]
myrecordpgshowcompdbcollection = mydb["RecordShowCompDB"]
myrecordpgshowusernamedbcollection = mydb["RecordShowUserNameDB"]
myrecordpgshowboxdbcollection = mydb["RecordShowBoxDB"]
myrecordpgshowkeynamedbcollection = mydb["RecordShowKeyNameDB"]
mymonthlysaveemailcollection = mydb["MonthlySaveEmailData"]
mycheckdaycollection = mydb["CheckUserInputDays"]
mykeynotreturnemailcollection = mydb["KeyNotReturnEmailData"]

myrecordpgshowdatedbcollection.insert_one({"user_id": 1, "starting_date": "mm/dd/yyyy", "ending_date": "mm/dd/yyyy"})
myrecordpgshowcompdbcollection.insert_one({"user_id": 1, "showcomp": ""})
myrecordpgshowusernamedbcollection.insert_one({"user_id": 1, "showusername": ""})
myrecordpgshowboxdbcollection.insert_one({"user_id": 1, "showbox": "ボックス 1"})
myrecordpgshowkeynamedbcollection.insert_one({"user_id": 1, "showkeyname": "Please Select"})
mymonthlysaveemailcollection.insert_one({"user_id": 1, "email1": "uhp070@obayashi.co.jp", "email2": "", "email3": "", "email4": ""})
mycheckdaycollection.insert_one({"user_id": 1, "daynum": "3"})
mykeynotreturnemailcollection.insert_one({"user_id": 1, "email1": "uhp070@obayashi.co.jp", "email2": "", "email3": "", "email4": ""})