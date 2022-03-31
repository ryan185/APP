import time, sys, pymongo, csv, os ,logging
from datetime import datetime

from save_log import get_log
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
#database
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myinfocollection = mydb["InfoData"]
myconditioncollection = mydb["ConditionData"]
mykanripart3dbcollection = mydb["KanriPart3DB"]
mydb2 = myclient['box2project']
mysignalb1collection = mydb2["SignalDataB1"]
mysignalb2collection = mydb2["SignalDataB2"]
mysignalb3collection = mydb2["SignalDataB3"]
mysignalb4collection = mydb2["SignalDataB4"]
myfacemodecollection = mydb["FaceMode"]

log_dir = 'C:\\Face\\log1'
os.chmod(log_dir,0o777)
filename = 'C:\\Face\\log1\\Mymodule.log'
get_log.setup_logger('log10', 'C:\\Face\\log1\\Mymodule.log')
logger_10 = logging.getLogger('log10')


class myclass(object):
	"""docstring for return_faceResult"""
	def __init__(self, arg):
		super(return_faceResult, self).__init__()
		self.arg = arg

	def ConditionZero():
		myconditioncollection.update_one({"user_id": 1},{'$set':{"condition":"0"}})
		myconditioncollection.update_one({"user_id": 2},{'$set':{"condition":"0"}})
		myconditioncollection.update_one({"user_id": 3},{'$set':{"condition":"0"}})
		myconditioncollection.update_one({"user_id": 4},{'$set':{"condition":"0"}})

	def CSVData():
		datalist = []

		inputfile = csv.reader(open("C:\\Face\\FaceData_key.csv",'r',encoding='UTF-8'))

		for i in inputfile:
			datalist = i

		# logger_10.info(datalist)
		# logger_10.info('CSVData')	
		return datalist

	def decideboxno(box_door_list):
		sendData = ""

		findFacemode = myfacemodecollection.find()
		for doc_mode in findFacemode:
			mode = doc_mode["mode"]

		if mode == "zeroOne":
			if len(box_door_list) == 10: #ZeroOne Mode
				box_door = box_door_list[9]
				if box_door == "1" or box_door == "１":
					sendData = "1"

				if box_door == "12" or box_door == "１２" or box_door == "21" or box_door == "２１":
					sendData = "12"
				if box_door == "13" or box_door == "１３" or box_door == "31" or box_door == "３１":
					sendData = "13"
				if box_door == "14" or box_door == "１４" or box_door == "41" or box_door == "４１":
					sendData = "14"

				if box_door == "124" or box_door == "１２４" or box_door == "142" or box_door == "１４２" or box_door == "214" or box_door == "２１４" or box_door == "241" or box_door == "２４１" or box_door == "421" or box_door == "４２１" or box_door == "412" or box_door == "４１２" :
					sendData = "124"
				if box_door == "123" or box_door == "１２３" or box_door == "132" or box_door == "１３２" or box_door == "321" or box_door == "３２１" or box_door == "312" or box_door == "３２１" or box_door == "213" or box_door == "２１３" or box_door == "231" or box_door == "２３１":
					sendData = "123"

				if box_door == "134" or box_door == "１３４" or box_door == "143" or box_door == "１４３" or box_door == "341" or box_door == "３４１" or box_door == "314" or box_door == "３１４" or box_door == "413" or box_door == "４１３" or box_door == "431" or box_door == "４３１":
					sendData = "134"

				if box_door == "234" or box_door == "２３４" or box_door == "243" or box_door == "２４３" or box_door == "324" or box_door == "３２４" or box_door == "342" or box_door == "３４２" or box_door == "423" or box_door == "４２３" or box_door == "432" or box_door == "４３２":
					sendData = "234"			

				if box_door == "2" or box_door == "２":
					sendData = "2"
				if box_door == "23" or box_door == "２３" or box_door == "23" or box_door == "３２":
					sendData = "23"
				if box_door == "24" or box_door == "２４" or box_door == "24" or box_door == "４２":
					sendData = "24"
				

				


				if box_door == "3" or box_door == "３":
					sendData = "3"
				if box_door == "34" or box_door == "３４" or box_door == "43" or box_door == "４３":
					sendData = "34"	
				if box_door == "4" or box_door == "４":
					sendData = "4"	
				if box_door == "0" or box_door == "０":



					# or box_door == "O"
					sendData = "ON"
			elif len(box_door_list) == 9:
				sendData = "OFF"
		
		if mode == "allboxes":
			if len(box_door_list) == 9: #全員Mode
				if "陌生人"  not in box_door_list:
					sendData = "ON"
			elif len(box_door_list) == 10:
				if "陌生人"  not in box_door_list:
					sendData = "ON"

		return sendData

	def FaceData():
		facelist = []
		# datalist = ['\ufeffKey', '/snapimg/2020/10/27/2020102716037648673173582.jpg', 'shun', '大林組', '0001', '2020-10-27 11:14:27', '0']
		datalist =[]
		inputfile = csv.reader(open("C:\\Face\\FaceData_key.csv",'r',encoding='UTF-8'))
		
		if "陌生人"  not in inputfile:
			inputfile = csv.reader(open("C:\\Face\\FaceData_key.csv",'r',encoding='UTF-8'))

			for i in inputfile:
				datalist = i
			
			# logger_10.info(datalist)
			# logger_10.info('FaceData')

			# print(len(datalist))
			# if len(datalist) == 1:
			# 	datalist = ['\ufeffKey', '/snapimg/2020/10/27/2020102716037648673173582.jpg', 'shun', '大林組', '0001', '2020-10-27 11:14:27', '0']




			if len(datalist) == 7:
				curr_user_name = datalist[2]
				facelist.append(curr_user_name)
				
				cur_dept_name = datalist[3]
				facelist.append(cur_dept_name)
				
				mydate = datalist[5]

				cur_dday = datetime.strptime(mydate, '%Y-%m-%d %H:%M:%S')
				facelist.append(cur_dday)

				cur_date_only = cur_dday.strftime("%Y-%m-%d")
				facelist.append(cur_date_only)

				cur_d_month = cur_dday.month
				facelist.append(cur_d_month)

				cur_d_day = cur_dday.day
				facelist.append(cur_d_day)

				cur_d_hour = cur_dday.strftime("%H")
				facelist.append(cur_d_hour)

				cur_d_min = cur_dday.strftime("%M")
				facelist.append(cur_d_min)

				cur_second = cur_dday.strftime("%S")
				facelist.append(cur_second)

				box_door = datalist[-1]
				facelist.append(box_door)

				# return facelist


			if len(datalist) == 6:
				curr_user_name = datalist[2]
				facelist.append(curr_user_name)
				
				cur_dept_name = datalist[3]
				facelist.append(cur_dept_name)
				
				mydate = datalist[5]

				cur_dday = datetime.strptime(mydate, '%Y-%m-%d %H:%M:%S')
				facelist.append(cur_dday)

				cur_date_only = cur_dday.strftime("%Y-%m-%d")
				facelist.append(cur_date_only)

				cur_d_month = cur_dday.month
				facelist.append(cur_d_month)

				cur_d_day = cur_dday.day
				facelist.append(cur_d_day)

				cur_d_hour = cur_dday.strftime("%H")
				facelist.append(cur_d_hour)

				cur_d_min = cur_dday.strftime("%M")
				facelist.append(cur_d_min)

				cur_second = cur_dday.strftime("%S")
				facelist.append(cur_second)

				# return facelist


			# logger_10.info(facelist)
			# logger_10.info('facelist')
			# print(facelist)
			return facelist

	def InfoData():
		infolist = []
		a = ['\ufeffKey', '/snapimg/2020/10/27/2020102716037648673173582.jpg', 'shun', '大林組', '0001', '2020-10-27 11:14:27', '0']

		inputfile = csv.reader(open("C:\\Face\\FaceData_key.csv",'r',encoding='UTF-8'))

		for j in inputfile:
			a = j
			
		curr_user_name = a[2]
		infolist.append(curr_user_name)
		cur_user_name = curr_user_name[0:4]
		infolist.append(cur_user_name)
		cur_dept_name = a[3]
		infolist.append(cur_dept_name)
		mydate = a[5]
		box_door = a[-1]
		cur_dday = datetime.strptime(mydate, '%Y-%m-%d %H:%M:%S')
		infolist.append(cur_dday)
		cur_date_only = cur_dday.strftime("%Y-%m-%d")
		infolist.append(cur_date_only)
		cur_d_month = cur_dday.month
		infolist.append(cur_d_month)
		cur_d_day = cur_dday.day
		infolist.append(cur_d_day)
		cur_d_hour = cur_dday.strftime("%H")
		infolist.append(cur_d_hour)
		cur_d_min = cur_dday.strftime("%M")
		infolist.append(cur_d_min)
		cur_second = cur_dday.strftime("%S")
		infolist.append(cur_second)

		return infolist

	def InfoUpdateNameComp(list1):
		myinfocollection.update_one({"user_id": 1},{'$set':{"fullname": list1[0],"name": list1[1], "dept_name": list1[2][:4],  "dept": list1[2], "dday": str(list1[3]), "date_only": list1[4], "d_month": str(list1[5]), "d_day": str(list1[6]), "d_hour": list1[7], "d_min": list1[8], "d_sec": list1[9]}})
		myinfocollection.update_one({"user_id": 2},{'$set':{"fullname": list1[0],"name": list1[1], "dept_name": list1[2][:4],  "dept": list1[2], "dday": str(list1[3]), "date_only": list1[4], "d_month": str(list1[5]), "d_day": str(list1[6]), "d_hour": list1[7], "d_min": list1[8], "d_sec": list1[9]}})
		myinfocollection.update_one({"user_id": 3},{'$set':{"fullname": list1[0],"name": list1[1], "dept_name": list1[2][:4],  "dept": list1[2], "dday": str(list1[3]), "date_only": list1[4], "d_month": str(list1[5]), "d_day": str(list1[6]), "d_hour": list1[7], "d_min": list1[8], "d_sec": list1[9]}})
		myinfocollection.update_one({"user_id": 4},{'$set':{"fullname": list1[0],"name": list1[1], "dept_name": list1[2][:4],  "dept": list1[2], "dday": str(list1[3]), "date_only": list1[4], "d_month": str(list1[5]), "d_day": str(list1[6]), "d_hour": list1[7], "d_min": list1[8], "d_sec": list1[9]}})

	def InfoUpdateBlank(list2):
		myinfocollection.update_one({"user_id": 1},{'$set':{"fullname": "","name": list2[1], "dept_name": list2[2][:4], "dept": "", "dday": str(list2[3]), "date_only": list2[4], "d_month": str(list2[5]), "d_day": str(list2[6]), "d_hour": list2[7], "d_min": list2[8], "d_sec": list2[9]}})
		myinfocollection.update_one({"user_id": 2},{'$set':{"fullname": "","name": list2[1], "dept_name": list2[2][:4], "dept": "", "dday": str(list2[3]), "date_only": list2[4], "d_month": str(list2[5]), "d_day": str(list2[6]), "d_hour": list2[7], "d_min": list2[8], "d_sec": list2[9]}})	
		myinfocollection.update_one({"user_id": 3},{'$set':{"fullname": "","name": list2[1], "dept_name": list2[2][:4], "dept": "", "dday": str(list2[3]), "date_only": list2[4], "d_month": str(list2[5]), "d_day": str(list2[6]), "d_hour": list2[7], "d_min": list2[8], "d_sec": list2[9]}})	
		myinfocollection.update_one({"user_id": 4},{'$set':{"fullname": "","name": list2[1], "dept_name": list2[2][:4], "dept": "", "dday": str(list2[3]), "date_only": list2[4], "d_month": str(list2[5]), "d_day": str(list2[6]), "d_hour": list2[7], "d_min": list2[8], "d_sec": list2[9]}})	