import os, signal, pymongo, psutil, sys, time, logging
import tkinter as tk, datetime
from save_log import get_log

#database
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
myapidbcollection = mydb["APIData"]
mycheckzebrapiddbcollection = mydb["CheckZebraPIDDB"]
myzebraalertcollection = mydb["ZEBRA"]


#log saving
get_log.setup_logger('log3', 'C:\\Face\\Log1\\CheckZebralog.log')
logger_3 = logging.getLogger('log3')

#code
class checkZebra():
	def getZebraPID(program):
		for zebrapid in psutil.pids():
			try:
				p = psutil.Process(zebrapid)
				if program in p.name():
					# print(zebrapid)
					# mycheckzebrapiddbcollection.update_one({"user_id": 1},{'$set':{"pid": zebrapid}}) 
					return zebrapid
				else:
					pass
			except:
				continue

	def check_running_or_not(exe_):
	    for pid in psutil.pids(): 
	        try:
	            p = psutil.Process(pid) 
	            if exe_ in p.name(): 
	                return True
	            else:
	                pass
	        except:
	            continue

	def run():
		log1 = True

		while True:
			try:
				findAPIStatus = myapidbcollection.find()
				for apidata_doc in findAPIStatus:
					checkapidata = apidata_doc["apidata"]
					datetimedata = apidata_doc["Date"]

				time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # str
				time1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S') # Datetime
				time2 = datetime.datetime.strptime(datetimedata, "%Y/%m/%d %H:%M:%S") # Datetime
				timediff = time1 - time2
				timediff = timediff.seconds
				# print(timediff)
				# if checkZebra.check_running_or_not('CS_RFID3_Host_Sample2.exe'):
				# 	myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 1}})
				# else:
				# 	myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 0}})

				if 0 <= timediff <= 60:	
					myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 1}})
					if checkapidata:
						if log1:
							logger_3.info('Database Result: '+str(checkapidata))
							logger_3.info('No error message in Zebra Application')
							log1 = False
						myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 1}})
					else:
						log1 = True
						myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 0}})
						logger_3.info('Database Result: '+str(checkapidata))
						logger_3.info('Some error occurred within Zebra Application')
						os.kill(checkZebra.getZebraPID('CS_RFID3_Host_Sample2.exe'), signal.SIGTERM)
						time.sleep(3)
						os.startfile("C:\\Program Files (x86)\\顔認証\\Setup1\\CS_RFID3_Host_Sample2.exe")
						logger_3.info('Zebra Software Closed and Reopened')
						time.sleep(10)
						# log1 = False
						
				else:
					if log1 :
						myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 0}})
						time.sleep(3)
						logger_3.info('Database Result: '+str(checkapidata))
						logger_3.info('Zebra Application is not opening/working')
						time.sleep(10)
						# print(checkZebra.check_running_or_not('CS_RFID3_Host_Sample2.exe'))
						if checkZebra.check_running_or_not('CS_RFID3_Host_Sample2.exe'):
							# print(checkZebra.getZebraPID('CS_RFID3_Host_Sample2.exe'))
							os.kill(checkZebra.getZebraPID('CS_RFID3_Host_Sample2.exe'), signal.SIGTERM)
							myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 0}})
							log1 = False
							time.sleep(10)
						# os.kill(checkZebra.getZebraPID('CS_RFID3_Host_Sample2.exe'), signal.SIGTERM)
						# time.sleep(3)	
						os.startfile("C:\\Program Files (x86)\\顔認証\\Setup1\\CS_RFID3_Host_Sample2.exe")
						myzebraalertcollection.update_one({"user_id": 1},{'$set':{"Error_code": 1}})
						logger_3.info('Zebra Software Got Opened Automatically')
						log1 = False
						time.sleep(24)
						
			except KeyboardInterrupt:
				logger_3.error("Manually interrupted by client user.")
				sys.exit()

			except Exception as e:
				logger_3.error(e)
				print(e)

# checkZebra.run()