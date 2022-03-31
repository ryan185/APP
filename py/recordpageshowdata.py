import pandas as pd, datetime, pymongo, json
from datetime import date 


myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myrecordpgshowdatedbcollection = mydb["RecordShowDateDB"]
myrecordpgshowcompdbcollection = mydb["RecordShowCompDB"]
myrecordpgshowusernamedbcollection = mydb["RecordShowUserNameDB"]
myrecordpgshowboxdbcollection = mydb["RecordShowBoxDB"]
myrecordpgshowkeynamedbcollection = mydb["RecordShowKeyNameDB"]

class get_recordshowdata(object):
	def __init__(self, arg):
		super(get_recordshowdata, self).__init__()
		self.arg = arg

	def output_list(uinlist, nolist):
		uin = uinlist
		# print(uin)
		numberlist = nolist
		showlist = []
		curr=str(date.today())
		print(curr)
		print("cuur")


		try:
			if len(uin) > 0:
				if "past" in uin:
					uin.remove('past')

				if "box1" in uin:
					myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "ボックス 1"}})
				if "box2" in uin:
					myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "ボックス 2"}})
				if "box3" in uin:
					myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "ボックス 3"}})
				if "box4" in uin:
					myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "ボックス 4"}})	
				if "all" in uin:
					myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "すべてのボックス"}})
				if "box1" not in uin and "box2" not in uin and "box3" not in uin and "box4" not in uin and "all" not in uin:
					myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "Please Select"}})

				if "today" in uin:
					# print("""""""""""""""1""""""""""""""")
					myrecordpgshowdatedbcollection.update_one({"user_id": 1},{'$set':{"starting_date": curr, "ending_date": curr}})
					if uin[3] != "":
						compnamefilt = uin[3]
						myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": compnamefilt}})
					else:
						myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": ""}})
					if uin[4] != "":
						usernamefilt = uin[4]
						myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": usernamefilt}})
					else:
						myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": ""}})
					if any(x in numberlist for x in uin):
						keynametofilter = uin[6]
						myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": keynametofilter}})
					else:
						myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": "Please Select"}})

				else:
					try:
						if datetime.datetime.strptime(uin[0], '%Y-%m-%d') or datetime.datetime.strptime(uin[1], '%Y-%m-%d'):
							myrecordpgshowdatedbcollection.update_one({"user_id": 1},{'$set':{"starting_date": uin[0], "ending_date": uin[1]}})
							if uin[2] != "":
								compnamefilt = uin[2]
								myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": compnamefilt}})
							else:
								myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": ""}})
							if uin[3] != "":
								usernamefilt = uin[3]
								myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": usernamefilt}})
							else:
								myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": ""}})
							if any(x in numberlist for x in uin):
								keynametofilter = uin[5]
								myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": keynametofilter}})
							else:
								myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": "Please Select"}})
					except Exception as e:
						print(e)
						# print("""""""""""""""2""""""""""""""")
						myrecordpgshowdatedbcollection.update_one({"user_id": 1},{'$set':{"starting_date": "mm/dd/yyyy", "ending_date": "mm/dd/yyyy"}})
						if uin[2] != "":
							compnamefilt = uin[2]
							myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": compnamefilt}})
						else:
							myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": ""}})
						if uin[3] != "":
							usernamefilt = uin[3]
							myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": usernamefilt}})
						else:
							myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": ""}})
						if any(x in numberlist for x in uin):
							keynametofilter = uin[5]
							myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": keynametofilter}})
						else:
							myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": "Please Select"}})

			else:
				# print("""""""""""""""3""""""""""""""")
				myrecordpgshowdatedbcollection.update_one({"user_id": 1},{'$set':{"starting_date": "mm/dd/yyyy", "ending_date": "mm/dd/yyyy"}})
				myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": ""}})
				myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": ""}})
				myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "Please Select"}})
				myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": "Please Select"}})

			findShowDate = myrecordpgshowdatedbcollection.find()
			findShowComp = myrecordpgshowcompdbcollection.find()
			findShowUsrName = myrecordpgshowusernamedbcollection.find()
			findShowKeyName = myrecordpgshowkeynamedbcollection.find()
			findShowBox = myrecordpgshowboxdbcollection.find()

			for doc_showdate in findShowDate:
				showlist.append(doc_showdate["starting_date"])
				showlist.append(doc_showdate["ending_date"])

			for doc_showcomp in findShowComp:
				showlist.append(doc_showcomp["showcomp"])

			for doc_showusername in findShowUsrName:
				showlist.append(doc_showusername["showusername"])

			for doc_showbox in findShowBox:
				showlist.append(doc_showbox["showbox"])

			for doc_showkeyname in findShowKeyName:
				showlist.append(doc_showkeyname["showkeyname"])

			showlist = json.dumps(showlist)

		except Exception as e:
			myrecordpgshowdatedbcollection.update_one({"user_id": 1},{'$set':{"starting_date": "mm/dd/yyyy", "ending_date": "mm/dd/yyyy"}})
			myrecordpgshowcompdbcollection.update_one({"user_id": 1},{'$set':{"showcomp": ""}})
			myrecordpgshowusernamedbcollection.update_one({"user_id": 1},{'$set':{"showusername": ""}})
			myrecordpgshowboxdbcollection.update_one({"user_id": 1},{'$set':{"showbox": "Please Select"}})
			myrecordpgshowkeynamedbcollection.update_one({"user_id": 1},{'$set':{"showkeyname": "Please Select"}})


			showlist = ["mm/dd/yyyy", "mm/dd/yyyy", "", "", ""]
			showlist = json.dumps(showlist)
		print(showlist)	
		return showlist

# numberlist = []
# todaydate = "2021-02-26"
# for i in range(1,101):
# 	numberlist.append(i)
# uin = ['2020-11-09', '2020-11-09', '', '', '', '']
# print(get_recordshowdata.output_list(uin, numberlist, todaydate))