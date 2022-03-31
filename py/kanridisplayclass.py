import pandas as pd
import pymongo
import json

myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
mysavedaycollection = mydb["SaveDayData"]
mysavehourcollection = mydb["SaveHourData"]
mysaveminutecollection = mydb["SaveMinuteData"]
mymonthlysaveemailcollection = mydb["MonthlySaveEmailData"]
mycheckdaycollection = mydb["CheckUserInputDays"]
mykeynotreturnemailcollection = mydb["KeyNotReturnEmailData"]
mykanripart3dbcollection = mydb["KanriPart3DB"]
mysysipdatadbcollection = mydb["SYSIPData"]
myipdatadbcollection = mydb["IPData"]
mykanripart2savehourcollection = mydb["KanriPart2SaveHourData"]
mykanripart2saveminutecollection = mydb["KanriPart2SaveMinuteData"]
myfacemodecollection = mydb["FaceMode"]



class get_kanrilist(object):
	"""docstring for get_kanrilist"""
	def __init__(self, arg):
		super(get_kanrilist, self).__init__()
		self.arg = arg

	def part1_list():
		part1list = []
		
		findSaveDay = mysavedaycollection.find()
		findSaveHour = mysavehourcollection.find()
		findSaveMinute = mysaveminutecollection.find()
		findEmailList = mymonthlysaveemailcollection.find()

		for doc_saveday in findSaveDay:
			part1list.append(doc_saveday["day"])

		for doc_savehour in findSaveHour:
			part1list.append(doc_savehour["hour"])

		for doc_saveminute in findSaveMinute:
			part1list.append(doc_saveminute["minute"])

		for doc_savemail in findEmailList:
			part1list.append(doc_savemail["email1"])
			part1list.append(doc_savemail["email2"])
			part1list.append(doc_savemail["email3"])
			part1list.append(doc_savemail["email4"])

		part1list = json.dumps(part1list)
		
		return part1list

	def part2_list():
		part2list = []
		#to find the day & hour & minute & Email from respective databases
		findDays = mycheckdaycollection.find()
		findHour = mykanripart2savehourcollection.find()
		findMinute = mykanripart2saveminutecollection.find()
		findEmailList = mykeynotreturnemailcollection.find()
		#to append the day & hour & minute & Email from respective databases to list
        
		for doc_days in findDays:
			part2list.append(doc_days["daynum"])
		for doc_hours in findHour:
			part2list.append(doc_hours["hour"])
		for doc_minutes in findMinute:
			part2list.append(doc_minutes["minute"])


		for doc_savemail in findEmailList:
			part2list.append(doc_savemail["email1"])
			part2list.append(doc_savemail["email2"])
			part2list.append(doc_savemail["email3"])
			part2list.append(doc_savemail["email4"])

		part2list = json.dumps(part2list)
		
		return part2list

	def part3_list():
		part3list = []

		findKanriPart3 = mykanripart3dbcollection.find()

		for doc_kanripart3 in findKanriPart3:
			part3list.append(doc_kanripart3["seconds"])

		part3list = json.dumps(part3list)
		
		return part3list

	def part4_list():
		part4list = []

		mydb2 = myclient['box2project']
		myantennab1collection = mydb2["AntennaDataB1"]
		myantennab2collection = mydb2["AntennaDataB2"]
		myantennab3collection = mydb2["AntennaDataB3"]
		myantennab4collection = mydb2["AntennaDataB4"]
		
		findAntennaB1 = myantennab1collection.find()
		findAntennaB2 = myantennab2collection.find()
		findAntennaB3 = myantennab3collection.find()
		findAntennaB4 = myantennab4collection.find()

		for doc_antenna in findAntennaB1:
			part4list.append(doc_antenna["antennaA"])
			part4list.append(doc_antenna["antennaB"])
		for doc_antenna in findAntennaB2:
			part4list.append(doc_antenna["antennaA"])
			part4list.append(doc_antenna["antennaB"])
		for doc_antenna in findAntennaB3:
			part4list.append(doc_antenna["antennaA"])
			part4list.append(doc_antenna["antennaB"])
		for doc_antenna in findAntennaB4:
			part4list.append(doc_antenna["antennaA"])
			part4list.append(doc_antenna["antennaB"])

		part4list = json.dumps(part4list)
		
		return part4list
	#To update the IPAddress	
	def part5_list():
	    part5list = []

	    findSysIP = mysysipdatadbcollection.find()
	    # findRPIP  = myipdatadbcollection.find()

	    for doc_kanripart5 in findSysIP:
	    	part5list.append(doc_kanripart5["sysip_address"])
	    # for doc_kanripart5 in findRPIP:
	    # 	part5list.append(doc_kanripart5["ip_address"])	
	    part5list = json.dumps(part5list)
	    return part5list

	def part6_list():
	    part6list = []

	    findmode = myfacemodecollection.find()
	    # findRPIP  = myipdatadbcollection.find()

	    for doc_kanripart6 in findmode:
	    	part6list.append(doc_kanripart6["mode"])
	    # for doc_kanripart5 in findRPIP:
	    # 	part5list.append(doc_kanripart5["ip_address"])	
	    part6list = json.dumps(part6list)
	    print(part6list) 
	    return part6list

# print(get_kanrilist.part1_list())
# print(get_kanrilist.part2_list())
# print(get_kanrilist.part3_list())
# print(get_kanrilist.part4_list())

