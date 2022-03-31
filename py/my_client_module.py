import  socket, time, sys, pymongo, csv, logging, os, threading
# import logging
# from mongolog.handlers import MongoHandler
from datetime import datetime
from pygame import mixer
from save_log import get_log
from mymodule import myclass
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

#database
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myinfocollection = mydb["InfoData"]
myconditioncollection = mydb["ConditionData"]
mykanripart3dbcollection = mydb["KanriPart3DB"]
myrpidatadbcollection = mydb["RpiData"]
mydb2 = myclient['box2project']
mysignalb1collection = mydb2["SignalDataB1"]
mysignalb2collection = mydb2["SignalDataB2"]
mysignalb3collection = mydb2["SignalDataB3"]
mysignalb4collection = mydb2["SignalDataB4"]
myipdatadbcollection = mydb["IPData"]
myrpicheckalertcollection = mydb["RPI"]
mycheckpipiddbcollection = mydb["CheckPIPIDDB"]

#log saving
# logger_2= logging.getLogger()
# logger_2.setLevel(logging.DEBUG)
# handler = TimedRotatingFileHandler('C:\\Face\\Log Folder\\Rpilog.log',when='M', interval = 1, backupCount=1, encoding='utf-8')
# handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
# logger_2.addHandler(handler)

log_dir = 'C:\\Face\\log1'
os.chmod(log_dir,0o777)
filename = 'C:\\Face\\log1\\Rpilog.log'
get_log.setup_logger('log2', 'C:\\Face\\log1\\Rpilog.log')
logger_2 = logging.getLogger('log2')
mixer.init()
mixer.music.load('C:\\Face\\mp3\\EK-01587.mp3')

class rpirun(object):
	"""docstring for rpirun"""
	def __init__(self, arg):
		super(rpirun, self).__init__()
		self.arg = arg

	def make_connection(port_):
		while True:
			try:
				#socket declaration
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				# sock.connect(('192.168.1.15', port_))
				# sock.connect(('192.168.1.112', port_))
				sock.connect(('192.168.1.228', port_))

				# logger_2.info('Connection Established with ' + '192.168.1.15' + ' ....')
				myrpicheckalertcollection.update_one({"user_id": 1},{'$set':{"RPIError_code": "1"}})
				# logger_2.info('Error code 1')
				return sock
			except:
				# logger_2.error('Failed to connect with host, trying to reconnect...')
				myrpicheckalertcollection.update_one({"user_id": 1},{'$set':{"RPIError_code": "0"}})
				# logger_2.error('ERRor code updated to 0')

	def sendreceive(server_1,server_2):
		filename = 'C:\\Face\\log1\\Rpilog.log'
		# fd = os.open(filename, os.O_WRONLY)
		case = var = log = alert = second1 = "1"
		sendData = receivedData = ""

		def playaudio():
			mixer.music.play(-1)
			time.sleep(3)

		while True:
			try:
				#number of seconds to send to rpi for alert red LED
				findSeconds = mykanripart3dbcollection.find()
				for seconds_doc in findSeconds:
					sendSeconds = seconds_doc["seconds"]

				#Port 12345 for sending "ON" and "OFF" datas
				server_1.send(sendData.encode())
				pid = os.getpid()
				mycheckpipiddbcollection.update_one({"user_id": 1},{'$set':{"pid": pid}})
				# print(pid)
				# print("PI Server 1")
				#Port 5000 for sending alert seconds
				server_2.send(str(sendSeconds).encode())
				
				#Will receive "box1", "box2", "box3", etc. from raspberry pi
				receivedData = server_1.recv(1024).decode()

				"""
				set condition variable to zero
				condition variable means the variable to remind HTML to display "更新中"
				if condition is 1, "更新中" will be displayed

				"""
				myclass.ConditionZero()

				#first time automatic open algorithm
				if receivedData == "Connected":
					logger_2.info(receivedData)
					logger_2.info('Program has started running....')
					logger_2.info('Received Message: \"'+ receivedData + "\"...")
					logger_2.info('Automatic open at the very first time....')
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": "ON"}})
					sendData = "ON"

				"""
				algorithm to count time to perform auto close
				auto close will occur when the user just did face recognition and none of the boxes is opened
				
				"""
				if receivedData == "StartTimeCount":
					# logger_2.info(receivedData)
					log = alert = "1" #variable to make sure that the following logs are saved for only once
					start_time = time.time()
					if var == "1":
						var = "0" #variable to make sure that ending time is saved for only once
						end_time = start_time+7

					if start_time > end_time and case == "1":
						case="0" #variable to make sure that "AutoClose" is sent for only once
						sendData="AutoClose"

				#algorithm to play alert audio when the door was opened for a long time
				if receivedData == "Alert_mp3_box1" or receivedData == "Alert_mp3_box2" or receivedData == "Alert_mp3_box3" or receivedData == "Alert_mp3_box4":
					# logger_2.info(receivedData)
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": receivedData}})
					# second1 = csvlist[8]
					if alert == "1":
						logger_2.warning('The door has been opened for more than ' + str(sendSeconds) + ' seconds....')
						t1 = threading.Thread(target=playaudio)
						t1.setDaemon(True)
						t1.start()
						alert = "0"

				#if the doors closed automatically, check face CSV file until when the user does face recognition again
				if receivedData == "SelfClosed":
					# logger_2.info(receivedData)
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": "SelfClosed"}})
					"""
					Empty Info database for user name and comopany 
					to make sure that name and company of user is not being displayed 
					on the right cornor text box of HTML page
					Info database is the database where user information from CSV file is saved one by one
					
					"""

					# logger_2.info(myclass.InfoUpdateBlank(myclass.InfoData()))
					myclass.InfoUpdateBlank(myclass.InfoData())

					#save log file telling the doors closed automatically
					# logger_2.info('LOG: \"'+ log + "\"...")
					if log == "1":
						logger_2.info('Received Message: \"'+ receivedData + "\"...")
						logger_2.info("Automatic system shutdown after 7 seconds...")
						logger_2.info("All 4 boxes has not been opened...")
						csvlist = myclass.FaceData()
						if (len(csvlist) == 10 or len(csvlist) == 9):
							second1 = csvlist[8]
							log = "0"
					
					#Query number of seconds from face recognition CSV
					# logger_2.info("if log is not 1")
					csvlist = myclass.FaceData()
					# logger_2.info(csvlist)
					# logger_2.info("All box close")
					if (len(csvlist) == 10 or len(csvlist) == 9):
							second2 = csvlist[8]
							# logger_2.info(second2)

					#compare the seconds and if the seconds are not the same, send "ON"
					# logger_2.info("compare the seconds and if the seconds are not the same")
					if second1 != second2:
						case = var = "1" #make the variables to "1" again since they are set to "0" above
						#update new user name and company to Info database to display them on HTML page 
						# sendData = "ON"
						#check door number to open and send that number to raspberry pi
						# logger_2.info("inside seconds  ")
						sendData = myclass.decideboxno(csvlist)
						myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})
						if sendData == "ON" or sendData == "1" or sendData == "2" or sendData == "3" or sendData == "4" or sendData == "12" or sendData == "13" or sendData == "14" or sendData == "123" or sendData == "124" or sendData == "134" or sendData == "23"or sendData == "24" or sendData == "234" or sendData == "34":
							#save csv data to log file
							logger_2.info(myclass.CSVData())
							logger_2.info("Previous Second: " + str(second1))
							logger_2.info("Current Second: " + str(second2))
							myclass.InfoUpdateNameComp(myclass.InfoData())
							logger_2.info("Sent \"" + sendData + "\" to Raspberry Pi...")
						#reset the seconds
						second1 = second2

				#if box1 is opened, send start stop API and display "更新中" on HTML page
				if receivedData == "box1":
					# logger_2.info(receivedData)
					mixer.music.pause()
					sendData = "OFF"
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})

					if log == "1":
						logger_2.info("Sent \"OFF\" to Raspberry Pi...")
						logger_2.info('Received Message: \"'+ receivedData + "\"...")
						logger_2.info("Box1 has been opened...")
					
						#update box1 api database to "Start"
						mysignalb1collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
						#update "更新中" database to "1" to display on HTML page
						myconditioncollection.update_one({"user_id": 1},{'$set':{"condition":"1"}})
						
						time.sleep(5)
						
						#update box1 api database to "Stop"
						mysignalb1collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
						#update "更新中" database to "0" to stop displaying on HTML page
						myconditioncollection.update_one({"user_id": 1},{'$set':{"condition":"0"}})
						#Empty name and company of the user again
						myclass.InfoUpdateBlank(myclass.InfoData())
						
						#wait for another 3 seconds to make a time gap between first and second door open process
						time.sleep(3)
						csvlist = myclass.FaceData()
						if (len(csvlist) == 10 or len(csvlist) == 9):
							second1 = csvlist[8]
						# logger_2.info('second1: \"'+ second1)

							log = "0"

					csvlist = myclass.FaceData()
					# logger_2.info(csvlist)
					# logger_2.info("Box1 open")
					if (len(csvlist) == 10 or len(csvlist) == 9):
						second2 = csvlist[8]
						# logger_2.info(second2)

					if second1 != second2:
						case = var = "1"
						# sendData = "ON"
						sendData = myclass.decideboxno(csvlist)
						myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})
						if sendData == "ON" or sendData == "1" or sendData == "2" or sendData == "3" or sendData == "4" or sendData == "12" or sendData == "13" or sendData == "14" or sendData == "123" or sendData == "124" or sendData == "134" or sendData == "23"or sendData == "24" or sendData == "234" or sendData == "34":
							logger_2.info(myclass.CSVData())
							logger_2.info("Previous Second: " + str(second1))
							logger_2.info("Current Second: " + str(second2))
							myclass.InfoUpdateNameComp(myclass.InfoData())
							logger_2.info("Sent \"" + sendData + "\" to Raspberry Pi...")
						second1 = second2

				if receivedData == "box2":
					# logger_2.info(receivedData)
					mixer.music.pause()
					sendData = "OFF"
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})

					if log == "1":
						logger_2.info("Sent \"OFF\" to Raspberry Pi...")
						logger_2.info('Received Message: \"'+ receivedData + "\"...")
						logger_2.info("Box2 has been opened...")

						mysignalb2collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
						myconditioncollection.update_one({"user_id": 2},{'$set':{"condition":"1"}})
						time.sleep(5)
						mysignalb2collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
						myconditioncollection.update_one({"user_id": 2},{'$set':{"condition":"0"}})
						myclass.InfoUpdateBlank(myclass.InfoData())
						time.sleep(3)
						csvlist = myclass.FaceData()

						if (len(csvlist) == 10 or len(csvlist) == 9):
						# print(csvlist)
						# logger_2.info(csvlist)
							second1 = csvlist[8]
						# logger_2.info('second1: \"'+ second1)
							log = "0"

					csvlist = myclass.FaceData()
					# logger_2.info(csvlist)
					# logger_2.info("Box2 open")
					if (len(csvlist) == 10 or len(csvlist) == 9):
							second2 = csvlist[8]
							# logger_2.info(second2)

					if second1 != second2:
						case = var = "1"
						# sendData = "ON"
						sendData = myclass.decideboxno(csvlist)
						myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})
						if sendData == "ON" or sendData == "1" or sendData == "2" or sendData == "3" or sendData == "4" or sendData == "12" or sendData == "13" or sendData == "14" or sendData == "123" or sendData == "124" or sendData == "134" or sendData == "23"or sendData == "24" or sendData == "234" or sendData == "34":
							logger_2.info(myclass.CSVData())
							logger_2.info("Previous Second: " + str(second1))
							logger_2.info("Current Second: " + str(second2))
							myclass.InfoUpdateNameComp(myclass.InfoData())
							logger_2.info("Sent \"" + sendData + "\" to Raspberry Pi...")
						second1 = second2

				if receivedData == "box3":
					# logger_2.info(receivedData)
					mixer.music.pause()
					sendData = "OFF"
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})

					if log == "1":
						logger_2.info("Sent \"OFF\" to Raspberry Pi...")
						logger_2.info('Received Message: \"'+ receivedData + "\"...")
						logger_2.info("Box3 has been opened...")

						mysignalb3collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
						myconditioncollection.update_one({"user_id": 3},{'$set':{"condition":"1"}})
						time.sleep(5)
						mysignalb3collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
						myconditioncollection.update_one({"user_id": 3},{'$set':{"condition":"0"}})
						myclass.InfoUpdateBlank(myclass.InfoData())
						time.sleep(3)
						csvlist = myclass.FaceData()
						if (len(csvlist) == 10 or len(csvlist) == 9):
						# logger_2.info(csvlist)
							second1 = csvlist[8]
						# logger_2.info('second1: \"'+ second1)
							log = "0"

					csvlist = myclass.FaceData()
					# logger_2.info(csvlist)
					# /logger_2.info("Box3 open")
					# print(csvlist)
					# print(len(csvlist))
					if (len(csvlist) == 10 or len(csvlist) == 9):
						second2 = csvlist[8]
						# logger_2.info(second2)

					if second1 != second2:
						case = var = "1"
						# sendData = "ON"
						sendData = myclass.decideboxno(csvlist)
						myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})
						if sendData == "ON" or sendData == "1" or sendData == "2" or sendData == "3" or sendData == "4" or sendData == "12" or sendData == "13" or sendData == "14" or sendData == "123" or sendData == "124" or sendData == "134" or sendData == "23"or sendData == "24" or sendData == "234" or sendData == "34":
							logger_2.info(myclass.CSVData())
							logger_2.info("Previous Second: " + str(second1))
							logger_2.info("Current Second: " + str(second2))
							myclass.InfoUpdateNameComp(myclass.InfoData())
							logger_2.info("Sent \"" + sendData + "\" to Raspberry Pi...")
						second1 = second2

				if receivedData == "box4":
					# logger_2.info(receivedData)
					mixer.music.pause()
					sendData = "OFF"
					myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})

					if log == "1":
						logger_2.info("Sent \"OFF\" to Raspberry Pi...")
						logger_2.info('Received Message: \"'+ receivedData + "\"...")
						logger_2.info("Box4 has been opened...")

						mysignalb4collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
						myconditioncollection.update_one({"user_id": 4},{'$set':{"condition":"1"}})
						time.sleep(5)
						mysignalb4collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
						myconditioncollection.update_one({"user_id": 4},{'$set':{"condition":"0"}})
						myclass.InfoUpdateBlank(myclass.InfoData())
						time.sleep(3)
						csvlist = myclass.FaceData()
						if (len(csvlist) == 10 or len(csvlist) == 9):
							second1 = csvlist[8]
						# logger_2.info(csvlist)
						# second1 = csvlist[8]
						# logger_2.info('second1: \"'+ second1)
							log = "0"

					csvlist = myclass.FaceData()
					# logger_2.info(csvlist)
					# logger_2.info("Box4 open")
					if (len(csvlist) == 10 or len(csvlist) == 9):
						second2 = csvlist[8]
						# logger_2.info(second2)


					if second1 != second2:
						case = var = "1"
						# sendData = "ON"
						sendData = myclass.decideboxno(csvlist)
						myrpidatadbcollection.update_one({"user_id": 1},{'$set':{"rpistatus": sendData}})
						if sendData == "ON" or sendData == "1" or sendData == "2" or sendData == "3" or sendData == "4" or sendData == "12" or sendData == "13" or sendData == "14" or sendData == "123" or sendData == "124" or sendData == "134" or sendData == "23"or sendData == "24" or sendData == "234" or sendData == "34":
							logger_2.info(myclass.CSVData())
							logger_2.info("Previous Second: " + str(second1))
							logger_2.info("Current Second: " + str(second2))
							myclass.InfoUpdateNameComp(myclass.InfoData())
							logger_2.info("Sent \"" + sendData + "\" to Raspberry Pi...")
						second1 = second2

				# os.close(fd)

			#for error handling "list index out of range" 	
			except IndexError as e:
				logger_2.error(e)
				logger_2.info("index error")
			
			#Perhaps for error handling "list index out of range" 
			except Exception as e:
				logger_2.error(e)
				s1 = rpirun.make_connection(12345)
				s2 = rpirun.make_connection(5000)
				rpirun.sendreceive(s1,s2)

# try:
# 	logger_2.info('Raspberry Pi Started...')

# 	s1 = rpirun.make_connection(12345)
# 	s2 = rpirun.make_connection(5000)

# 	rpirun.sendreceive(s1,s2)
# except Exception as e:
# 	logger_2.error(e)