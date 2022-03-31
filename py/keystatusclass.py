import pandas as pd
import pymongo
import json

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myKeycollection = mydb["SampleKeyData"]
myTempKeycollection = mydb["TemporaryKeyData"]
mykeynamecollection = mydb["KeyNameData"]
mynamecollection = mydb["SampleNameData"]
mydeptcollection= mydb["SampleDeptData"]
mydaycollection = mydb["SampleDayData"]
mymonthcollection = mydb["SampleMonthData"]
myhourcollection = mydb["SampleHourData"]
myminutecollection = mydb["SampleMinuteData"]
mykeycolorcollection = mydb["KeyColorData"]
mynokeycolorcollection = mydb["NoKeyColorData"]
mykeyIdcollection = mydb["KeyIdData"]
mykeyboxcollection = mydb["KeyBoxData"]
myrentalcompanycollection = mydb["RentalCompanyData"]
myrentalcompanyidcollection = mydb["RentalCompanyIdData"]
myRoomcollection = mydb["RoomData"]
myStatuscollection = mydb["KeyStatus"]



class get_list(object):
	"""docstring for get_percentage"""
	def __init__(self, arg):
		super(get_record, self).__init__()
		self.arg = arg

	def name_list(id_):
		namelist = []
		findName = mynamecollection.find(filter = { "user_id" : id_})

		for doc_name in findName:
			for i in range(1,101):
				namelist.insert(i-1, doc_name["name%i" %i])

		namelist = json.dumps(namelist)
		
		return namelist

	def keyname_list(id_):
		keynamelist = []
		findKeyName = mykeynamecollection.find(filter = { "user_id" : id_})

		for doc_keyname in findKeyName:
			for i in range(1,101):
				check = doc_keyname["keyname%i" %i]
				if check != "-":
					if i <= 9:
						string = "00%i" %i + "<br>" + check[:15]
						keynamelist.insert(i-1, string)
					elif i <= 99:
						string = "0%i" %i + "<br>" + check[:15]
						keynamelist.insert(i-1, string)
					elif i == 100:
						string = "100" + "<br>" + check[:15]
						keynamelist.insert(i-1, string)
				else:
					keynamelist.insert(i-1, check[:10])

		keynamelist = json.dumps(keynamelist)
		
		return keynamelist

	def compname_list(id_):
		complist = []
		findDept = mydeptcollection.find(filter = { "user_id" : id_})

		for doc_dept in findDept:
			for i in range(1,101):
				complist.insert(i-1,doc_dept["dept%i" %i])

		complist = json.dumps(complist)
		
		return complist

	def month_list(id_):
		monthlist = []
		findMonth = mymonthcollection.find(filter = { "user_id" : id_})

		for doc_month in findMonth:
			for i in range(1,101):
				monthlist.insert(i-1,doc_month["month%i" %i])

		monthlist = json.dumps(monthlist)
		
		return monthlist

	def day_list(id_):
		daylist = []
		findDay = mydaycollection.find(filter = { "user_id" : id_})
		
		for doc_day in findDay:
			for i in range(1,101):
				daylist.insert(i-1,doc_day["day%i" %i])

		daylist = json.dumps(daylist)
		
		return daylist

	def hour_list(id_):
		hourlist = []
		findHour = myhourcollection.find(filter = { "user_id" : id_})

		for doc_hour in findHour:
			for i in range(1,101):
				hourlist.insert(i-1,doc_hour["hour%i" %i])

		hourlist = json.dumps(hourlist)
		
		return hourlist

	def minute_list(id_):
		minutelist = []
		findMinute = myminutecollection.find(filter = { "user_id" : id_})

		for doc_minute in findMinute:
			for i in range(1,101):
				minutelist.insert(i-1,doc_minute["minute%i" %i])

		minutelist = json.dumps(minutelist)
		
		return minutelist

	def keycolor_list(id_):
		keycolorlist = []
		findKeyColor = mykeycolorcollection.find(filter = { "user_id" : id_})

		for doc_epckeycolor in findKeyColor:
			for i in range(1,101):
				keycolorlist.insert(i-1,doc_epckeycolor["keycolor%i" %i])

		keycolorlist = json.dumps(keycolorlist)
		
		return keycolorlist

	def nokeycolor_list(id_):
		nokeycolorlist = []
		findNoKeyColor = mynokeycolorcollection.find(filter = { "user_id" : id_})

		for doc_epcnokeycolor in findNoKeyColor:
			for i in range(1,101):
				nokeycolorlist.insert(i-1,doc_epcnokeycolor["keycolor%i" %i])

		nokeycolorlist = json.dumps(nokeycolorlist)
		
		return nokeycolorlist

	def key_list(id_):
		keylist = []
		findKey = myKeycollection.find(filter = { "user_id" : id_})

		for doc_key in findKey:
			for i in range(1,101):
				keylist.insert(i-1,doc_key["Tag%i" %i])

		keylist = json.dumps(keylist)
		
		return keylist

	def tempkey_list(id_):
		tempkeylist = []
		findTempKey = myTempKeycollection.find(filter = { "user_id" : id_})

		for doc_tempkey in findTempKey:
			for i in range(1,101):
				tempkeylist.insert(i-1,doc_tempkey["Tag%i" %i])

		tempkeylist = json.dumps(tempkeylist)
		
		return tempkeylist

	####   Python   ####

	def epckey_list(id_):
		epckeylist = []
		findKey = myKeycollection.find(filter = { "user_id" : id_})

		for doc_key in findKey:
			for i in range(1,101):
				epckeylist.insert(i-1,doc_key["Tag%i" %i])

		return epckeylist

	def tempepckey_list(id_):
		tempepckeylist = []
		findTempKey = myTempKeycollection.find(filter = { "user_id" : id_})

		for doc_tempkey in findTempKey:
			for i in range(1,101):
				tempepckeylist.insert(i-1,doc_tempkey["Tag%i" %i])

		return tempepckeylist

	def epcname_list(id_):
		epcnamelist = []
		findKeyName = mykeynamecollection.find(filter = { "user_id" : id_})

		for doc_keyname in findKeyName:
			for i in range(1,101):
				check = doc_keyname["keyname%i" %i]
				if check != "-":
					if i <= 9:
						string = "00%i" %i + " " + check
						epcnamelist.insert(i-1, string)
					elif i <= 99:
						string = "0%i" %i + " " + check
						epcnamelist.insert(i-1, string)
					elif i == 100:
						string = "100" + " " + check
						epcnamelist.insert(i-1, string)
				else:
					epcnamelist.insert(i-1, check)

		return epcnamelist

	def keyid_list(id_):
		keyidlist = []
		findKeyId = mykeyIdcollection.find(filter = { "user_id" : id_})

		for doc_keyId in findKeyId:
			for i in range(1,101):
				keyidlist.insert(i-1,doc_keyId["keyId%i" %i])

		return keyidlist

	def epckeybox_list(id_):
		epckeyboxlist = []
		findKeyBox = mykeyboxcollection.find(filter = { "user_id" : id_})

		for doc_keybox in findKeyBox:
			for i in range(1,101):
				epckeyboxlist.insert(i-1,doc_keybox["keybox%i" %i])

		return epckeyboxlist

	def rentcomp_list(id_):
		rentcomplist = []
		findRentalComp = myrentalcompanycollection.find(filter = { "user_id" : id_})

		for doc_rentcomp in findRentalComp:
			for i in range(1,101):
				rentcomplist.insert(i-1,doc_rentcomp["rentcomp%i" %i])

		return rentcomplist

	def rentcompid_list(id_):
		rentcompidlist = []
		findRentalCompId = myrentalcompanyidcollection.find(filter = { "user_id" : id_})

		for doc_rentcompid in findRentalCompId:
			for i in range(1,101):
				rentcompidlist.insert(i-1,doc_rentcompid["rentcompid%i" %i])

		return rentcompidlist

	def roomid_list(id_):
		roomidlist = []
		findRoomId = myRoomcollection.find(filter = { "user_id" : id_})

		for doc_roomidlist in findRoomId:
			for i in range(1,101):
				roomidlist.insert(i-1,doc_roomidlist["Room%i" %i])

		return roomidlist

	def statusid_list(id_):
		statusidlist = []
		findStatusId = myStatuscollection.find(filter = { "user_id" : id_})

		for doc_statusidlist in findStatusId:
			for i in range(1,101):
				statusidlist.insert(i-1,doc_statusidlist["Status%i" %i])

		return statusidlist


# uinlist = ['2020-03-24', '2020-04-10', '大林組', 'シュンレイ', 'box2', '010 5.8M', 'returned', '50']
# keyid = ""
# yesorno = "No"
# start_date = '2020-03-24'
# stop_date = '2020-04-10'
# filterlist = ['twodates', 'returned']
# keyname = '010 5.8M'
# comp = '大林組'
# user = 'シュンレイ'
# df=get_record.output_df(uinlist,keyid,yesorno,start_date,stop_date,filterlist,keyname,comp,user)
# print(df)
