from flask import Flask, render_template, request, url_for, redirect, send_file
from flask import jsonify
from livereload import Server
from werkzeug.utils import secure_filename
import schedule
import pandas as pd, numpy as np, pymongo, os
from datetime import datetime, timedelta, date 
import timeit, time, json, csv, logging, threading
from keystatusclass import get_list
from recordclass import get_record
from graphclass import get_graph
from downloadpdf import get_pdf
from my_client_module import rpirun
from recordpageshowdata import get_recordshowdata
from save_log import get_log
from kanridisplayclass import get_kanrilist
from kanripart1 import kanri_part1_sendEmailMonthly
from kanripart2 import kanri_part2_run
from start_stop_zebra import checkZebra
from threading import Timer
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

#Flask application configuration
app = Flask(__name__, instance_relative_config=True)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#Database Declaration
myclient = pymongo.MongoClient("localhost", 27017)
mydb = myclient['key']
mynamecollection = mydb["SampleNameData"]
mydeptcollection= mydb["SampleDeptData"]
mydaycollection = mydb["SampleDayData"]
mymonthcollection = mydb["SampleMonthData"]
myhourcollection = mydb["SampleHourData"]
myminutecollection = mydb["SampleMinuteData"]
myKeycollection = mydb["SampleKeyData"]
myTempKeycollection = mydb["TemporaryKeyData"]
mykeynamecollection = mydb["KeyNameData"]
mykeyIdcollection = mydb["KeyIdData"]
mykeyboxcollection = mydb["KeyBoxData"]
mykeycolorcollection = mydb["KeyColorData"]
mynokeycolorcollection = mydb["NoKeyColorData"]
myrentalcompanycollection = mydb["RentalCompanyData"]
myrentalcompanyidcollection = mydb["RentalCompanyIdData"]
mycheckboxcollection = mydb["RegPageBoxData"]
mytempepccountcollection = mydb["TempEPCCountData"]
mystatecollection = mydb["StateData"]
mycheckcollection = mydb["CheckData"]
myconditioncollection = mydb["ConditionData"]
mysituationcollection = mydb["SituationData"]
mystatuscollection = mydb["StatusData"]
myinfocollection = mydb["InfoData"]
mysavedaycollection = mydb["SaveDayData"]
mysavehourcollection = mydb["SaveHourData"]
mysaveminutecollection = mydb["SaveMinuteData"]
mynumbercollection = mydb["RecordDBNumber"]
myrecordcollection = mydb["RecordDatabase1"]
mykagipiddbcollection = mydb["KagiPIDDB"]
myfacemodecollection = mydb["FaceMode"]
myrpidatadbcollection = mydb["RpiData"]
mysysipdatadbcollection = mydb["SYSIPData"]
myipdatadbcollection = mydb["IPData"]
myzebraalertcollection = mydb["ZEBRA"]
myrpicheckalertcollection = mydb["RPI"]
mymonthlysaveemailcollection = mydb["MonthlySaveEmailData"]
mykeynotreturnemailcollection = mydb["KeyNotReturnEmailData"]
mykanripart2savehourcollection = mydb["KanriPart2SaveHourData"]
mykanripart2saveminutecollection = mydb["KanriPart2SaveMinuteData"]
mycheckzebrapiddbcollection = mydb["CheckZebraPIDDB"]
mydatacollection = mydb["DataDB"]
myprocessflowdbcollection = mydb["ProcessFlowDB"]
myStatuscollection = mydb["KeyStatus"]



log_dir = 'C:\\Face\\log1'
os.chmod(log_dir, 0o777)
get_log.setup_logger('log1', 'C:\\Face\\log1\\PureMainPage.log')
logger_1 = logging.getLogger('log1')

for i in range(1,16):
	myrecordcollection = mydb["RecordDatabase%i" %i]
	number = myrecordcollection.estimated_document_count()
	if number < 10000:
		myrecordcollection = mydb["RecordDatabase%i" %i]
		mynumbercollection.update_one({"user_id": 1},{'$set':{"num":i}})
		logger_1.info('Currently using database %i...' %i)
		break


#Create routing to html Home Page
@ app.route ('/')
def function():
	logger_1.info('Home Page')
	return render_template('homepage.html') 

@ app.route ('/box1') 
def box1():
	findInfo = myinfocollection.find(filter = { "user_id" : 1})
	for doc_info in findInfo:
		fullname=doc_info["fullname"]
		name=doc_info["name"]
		dept_name=doc_info["dept_name"]
		dept=doc_info["dept"]
		dday=doc_info["dday"]
		date_only=doc_info["date_only"]
		d_month=doc_info["d_month"]
		d_day=doc_info["d_day"]
		d_hour=doc_info["d_hour"]
		d_min=doc_info["d_min"]
		d_sec=doc_info["d_sec"]
		currsecond=d_sec

	#Assign individual variable to Take Out the Data from each Database Collection
	findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 1})
	findState = mystatecollection.find(filter = { "user_id" : 1})
	findCheck = mycheckcollection.find(filter = { "user_id" : 1})
	findCondition = myconditioncollection.find(filter = { "user_id" : 1})
	findStatus = myStatuscollection.find(filter = { "user_id" : 1})
	findRpiData = myrpidatadbcollection.find()
	findZebraData = myzebraalertcollection.find()
	findRPIError  = myrpicheckalertcollection.find()

	#python list
	epckeylist     = get_list.epckey_list(1)
	epcnamelist    = get_list.epcname_list(1)
	epckeyboxlist  = get_list.epckeybox_list(1)
	keyidlist      = get_list.keyid_list(1)
	rentcomplist   = get_list.rentcomp_list(1)
	rentcompidlist = get_list.rentcompid_list(1)
	roomidlist     = get_list.roomid_list(1)
	statusidlist   = get_list.statusid_list(1)

	#html list
	keynamelist   = get_list.keyname_list(1)
	namelist      = get_list.name_list(1)
	compnamelist  = get_list.compname_list(1)
	monthlist     = get_list.month_list(1)
	daylist       = get_list.day_list(1)
	hourlist      = get_list.hour_list(1)
	minutelist    = get_list.minute_list(1)
	keycolorlist  = get_list.keycolor_list(1)
	nokeycolorlist  = get_list.nokeycolor_list(1)
	firstkeylist  = get_list.key_list(1)
	secondkeylist = get_list.key_list(1)


	#condition variables
	for doc_state in findState:
		state=doc_state["state"]

	for doc_check in findCheck:
		check=doc_check["check"]

	for doc_condition in findCondition:
		condition=doc_condition["condition"]

	#greenred 
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]
    #for green red notification Zebra and PI are connected
	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]
		# logger_1.error(rpierror)	

	if condition=="0":
		mycheckcollection.update_one({"user_id": 1},{'$set':{"check": "1"}})
		mystatecollection.update_one({"user_id": 1},{'$set':{"state": "1"}})
	# print(condition)

	if condition=="1" and state=="1":
		logger_1.info('Box1 has been opened...')
		# print(condition)
		if check=="1":
			logger_1.info('Checking the keys and Updating the Page...')
			mycheckcollection.update_one({"user_id": 1},{'$set':{"check": "0"}})
			return render_template('box1updating.html', show_name=dept, show_dept=fullname, namelist=namelist, 
			keynamelist=keynamelist, compnamelist=compnamelist, monthlist=monthlist, daylist=daylist, 
			hourlist=hourlist, minutelist=minutelist, keycolorlist =keycolorlist, nokeycolorlist=nokeycolorlist, firstkeylist=firstkeylist, 
			secondkeylist=secondkeylist,Error_code=zebradata,RPIError_code=rpierror)

		time.sleep(5.5)

		
		mystatecollection.update_one({"user_id": 1},{'$set':{"state": "0"}})

	#html list
	ukeylist       = get_list.tempkey_list(1)
	unamelist      = get_list.name_list(1)
	ucompnamelist  = get_list.compname_list(1)
	umonthlist     = get_list.month_list(1)
	udaylist       = get_list.day_list(1)
	uhourlist      = get_list.hour_list(1)
	uminutelist    = get_list.minute_list(1)
	ukeycolorlist  = get_list.keycolor_list(1)
	unokeycolorlist  = get_list.nokeycolor_list(1)

	#greenred 
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

    #for green red notification Zebra and PI are connected
	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]
		# logger_1.error(rpierror)

	return render_template('box1.html', show_name=dept, show_dept=fullname, namelist=unamelist,  rpi=rpidata,
	compnamelist=ucompnamelist, monthlist=umonthlist, daylist=udaylist, hourlist=uhourlist, keynamelist=keynamelist, 
	minutelist=uminutelist, keycolorlist=ukeycolorlist, nokeycolorlist=unokeycolorlist, firstkeylist=firstkeylist, secondkeylist=ukeylist,Error_code=zebradata,RPIError_code=rpierror)



@ app.route ('/box2') 
def box2():
	findInfo = myinfocollection.find(filter = { "user_id" : 2})
	for doc_info in findInfo:
		fullname=doc_info["fullname"]
		name=doc_info["name"]
		dept_name=doc_info["dept_name"]
		dept=doc_info["dept"]
		dday=doc_info["dday"]
		date_only=doc_info["date_only"]
		d_month=doc_info["d_month"]
		d_day=doc_info["d_day"]
		d_hour=doc_info["d_hour"]
		d_min=doc_info["d_min"]
		d_sec=doc_info["d_sec"]
		currsecond=d_sec

	#Assign individual variable to Take Out the Data from each Database Collection
	findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 2})
	findState = mystatecollection.find(filter = { "user_id" : 2})
	findCheck = mycheckcollection.find(filter = { "user_id" : 2})
	findCondition = myconditioncollection.find(filter = { "user_id" : 2})
	findRpiData = myrpidatadbcollection.find()
	findZebraData = myzebraalertcollection.find()
	findRPIError  = myrpicheckalertcollection.find()

	#python list
	epckeylist     = get_list.epckey_list(2)
	epcnamelist    = get_list.epcname_list(2)
	epckeyboxlist  = get_list.epckeybox_list(2)
	keyidlist      = get_list.keyid_list(2)
	rentcomplist   = get_list.rentcomp_list(2)
	rentcompidlist = get_list.rentcompid_list(2)
	roomidlist     = get_list.roomid_list(2)

	#html list
	keynamelist   = get_list.keyname_list(2)
	namelist      = get_list.name_list(2)
	compnamelist  = get_list.compname_list(2)
	monthlist     = get_list.month_list(2)
	daylist       = get_list.day_list(2)
	hourlist      = get_list.hour_list(2)
	minutelist    = get_list.minute_list(2)
	keycolorlist  = get_list.keycolor_list(2)
	nokeycolorlist  = get_list.nokeycolor_list(2)
	firstkeylist  = get_list.key_list(2)
	secondkeylist = get_list.key_list(2)

	#condition variables
	for doc_state in findState:
		state=doc_state["state"]

	for doc_check in findCheck:
		check=doc_check["check"]

	for doc_condition in findCondition:
		condition=doc_condition["condition"]

	#greenred
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]
		# logger_1.error(rpierror)	

	if condition=="0":
		mycheckcollection.update_one({"user_id": 2},{'$set':{"check": "1"}})
		mystatecollection.update_one({"user_id": 2},{'$set':{"state": "1"}})

	if condition=="1" and state=="1":
		logger_1.info('Box2 has been opened...')
		if check=="1":
			logger_1.info('Checking the keys and Updating the Page...')
			mycheckcollection.update_one({"user_id": 2},{'$set':{"check": "0"}})
			return render_template('box2updating.html', show_name=dept, show_dept=fullname, namelist=namelist, 
			keynamelist=keynamelist, compnamelist=compnamelist, monthlist=monthlist, daylist=daylist, 
			hourlist=hourlist, minutelist=minutelist, keycolorlist =keycolorlist, nokeycolorlist=nokeycolorlist, firstkeylist=firstkeylist, 
			secondkeylist=secondkeylist,Error_code=zebradata,RPIError_code=rpierror)

		time.sleep(5.5)

		

		mystatecollection.update_one({"user_id": 2},{'$set':{"state": "0"}})

	#html list
	ukeylist       = get_list.tempkey_list(2)
	unamelist      = get_list.name_list(2)
	ucompnamelist  = get_list.compname_list(2)
	umonthlist     = get_list.month_list(2)
	udaylist       = get_list.day_list(2)
	uhourlist      = get_list.hour_list(2)
	uminutelist    = get_list.minute_list(2)
	ukeycolorlist  = get_list.keycolor_list(2)
	unokeycolorlist  = get_list.nokeycolor_list(2)

	#greenred
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]
		# logger_1.error(rpierror)

	return render_template('box2.html', show_name=dept, show_dept=fullname, namelist=unamelist,  rpi=rpidata,
	compnamelist=ucompnamelist, monthlist=umonthlist, daylist=udaylist, hourlist=uhourlist, keynamelist=keynamelist, 
	minutelist=uminutelist, keycolorlist=ukeycolorlist, nokeycolorlist=unokeycolorlist, firstkeylist=firstkeylist, secondkeylist=ukeylist,Error_code=zebradata,RPIError_code=rpierror)




@ app.route ('/box3') 
def box3():
	findInfo = myinfocollection.find(filter = { "user_id" : 3})
	Room=[]
	# print(type(findInfo))
	for doc_info in findInfo:
		fullname=doc_info["fullname"]
		name=doc_info["name"]
		dept_name=doc_info["dept_name"]
		dept=doc_info["dept"]
		dday=doc_info["dday"]
		date_only=doc_info["date_only"]
		d_month=doc_info["d_month"]
		d_day=doc_info["d_day"]
		d_hour=doc_info["d_hour"]
		d_min=doc_info["d_min"]
		d_sec=doc_info["d_sec"]
		currsecond=d_sec

	#Assign individual variable to Take Out the Data from each Database Collection
	findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 3})
	findState = mystatecollection.find(filter = { "user_id" : 3})
	findCheck = mycheckcollection.find(filter = { "user_id" : 3})
	findCondition = myconditioncollection.find(filter = { "user_id" : 3})
	findRpiData = myrpidatadbcollection.find()
	findZebraData = myzebraalertcollection.find()
	findRPIError  = myrpicheckalertcollection.find()


	#python list
	epckeylist     = get_list.epckey_list(3)
	epcnamelist    = get_list.epcname_list(3)
	epckeyboxlist  = get_list.epckeybox_list(3)
	keyidlist      = get_list.keyid_list(3)
	rentcomplist   = get_list.rentcomp_list(3)
	rentcompidlist = get_list.rentcompid_list(3)
	roomidlist     = get_list.roomid_list(3)

	#html list
	keynamelist   = get_list.keyname_list(3)
	namelist      = get_list.name_list(3)
	compnamelist  = get_list.compname_list(3)
	monthlist     = get_list.month_list(3)
	daylist       = get_list.day_list(3)
	hourlist      = get_list.hour_list(3)
	minutelist    = get_list.minute_list(3)
	keycolorlist  = get_list.keycolor_list(3)
	nokeycolorlist  = get_list.nokeycolor_list(3)
	firstkeylist  = get_list.key_list(3)
	secondkeylist = get_list.key_list(3)

	#condition variables
	for doc_state in findState:
		state=doc_state["state"]

	for doc_check in findCheck:
		check=doc_check["check"]

	for doc_condition in findCondition:
		condition=doc_condition["condition"]

	#greenred
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]		

	if condition=="0":
		mycheckcollection.update_one({"user_id": 3},{'$set':{"check": "1"}})
		mystatecollection.update_one({"user_id": 3},{'$set':{"state": "1"}})

	if condition=="1" and state=="1":
		logger_1.info('Box3 has been opened...')
		if check=="1":
			logger_1.info('Checking the keys and Updating the Page...')
			mycheckcollection.update_one({"user_id": 3},{'$set':{"check": "0"}})
			return render_template('box3updating.html', show_name=dept, show_dept=fullname, namelist=namelist, 
			keynamelist=keynamelist, compnamelist=compnamelist, monthlist=monthlist, daylist=daylist, 
			hourlist=hourlist, minutelist=minutelist, keycolorlist =keycolorlist, nokeycolorlist=nokeycolorlist, firstkeylist=firstkeylist, 
			secondkeylist=secondkeylist,Error_code=zebradata,RPIError_code=rpierror)

		time.sleep(5.5)
			
		

		
		mystatecollection.update_one({"user_id": 3},{'$set':{"state": "0"}})

	

	#html list
	ukeylist       = get_list.tempkey_list(3)
	unamelist      = get_list.name_list(3)
	ucompnamelist  = get_list.compname_list(3)
	umonthlist     = get_list.month_list(3)
	udaylist       = get_list.day_list(3)
	uhourlist      = get_list.hour_list(3)
	uminutelist    = get_list.minute_list(3)
	ukeycolorlist  = get_list.keycolor_list(3)
	unokeycolorlist  = get_list.nokeycolor_list(3)

	#greenred
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]
	return render_template('box3.html', show_name=dept, show_dept=fullname, namelist=unamelist,  rpi=rpidata,
	compnamelist=ucompnamelist, monthlist=umonthlist, daylist=udaylist, hourlist=uhourlist, keynamelist=keynamelist, 
	minutelist=uminutelist, keycolorlist=ukeycolorlist, nokeycolorlist=unokeycolorlist, firstkeylist=firstkeylist, secondkeylist=ukeylist,Error_code=zebradata,RPIError_code=rpierror)



@ app.route ('/box4') 
def box4():
	findInfo = myinfocollection.find(filter = { "user_id" : 4})
	for doc_info in findInfo:
		fullname=doc_info["fullname"]
		name=doc_info["name"]
		dept_name=doc_info["dept_name"]
		dept=doc_info["dept"]
		dday=doc_info["dday"]
		date_only=doc_info["date_only"]
		d_month=doc_info["d_month"]
		d_day=doc_info["d_day"]
		d_hour=doc_info["d_hour"]
		d_min=doc_info["d_min"]
		d_sec=doc_info["d_sec"]
		currsecond=d_sec

	#Assign individual variable to Take Out the Data from each Database Collection
	findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 4})
	findState = mystatecollection.find(filter = { "user_id" : 4})
	findCheck = mycheckcollection.find(filter = { "user_id" : 4})
	findCondition = myconditioncollection.find(filter = { "user_id" : 4})
	findRpiData = myrpidatadbcollection.find()
	findZebraData = myzebraalertcollection.find()
	findRPIError  = myrpicheckalertcollection.find()


	#python list
	epckeylist     = get_list.epckey_list(4)
	epcnamelist    = get_list.epcname_list(4)
	epckeyboxlist  = get_list.epckeybox_list(4)
	keyidlist      = get_list.keyid_list(4)
	rentcomplist   = get_list.rentcomp_list(4)
	rentcompidlist = get_list.rentcompid_list(4)
	roomidlist     = get_list.roomid_list(4)

	#html list
	keynamelist   = get_list.keyname_list(4)
	namelist      = get_list.name_list(4)
	compnamelist  = get_list.compname_list(4)
	monthlist     = get_list.month_list(4)
	daylist       = get_list.day_list(4)
	hourlist      = get_list.hour_list(4)
	minutelist    = get_list.minute_list(4)
	keycolorlist  = get_list.keycolor_list(4)
	nokeycolorlist  = get_list.nokeycolor_list(4)
	firstkeylist  = get_list.key_list(4)
	secondkeylist = get_list.key_list(4)

	#condition variables
	for doc_state in findState:
		state=doc_state["state"]

	for doc_check in findCheck:
		check=doc_check["check"]

	for doc_condition in findCondition:
		condition=doc_condition["condition"]

	#greenred
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]	

	if condition=="0":
		mycheckcollection.update_one({"user_id": 4},{'$set':{"check": "1"}})
		mystatecollection.update_one({"user_id": 4},{'$set':{"state": "1"}})

	if condition=="1" and state=="1":
		logger_1.info('Box4 has been opened...')
		if check=="1":
			logger_1.info('Checking the keys and Updating the Page...')
			mycheckcollection.update_one({"user_id": 4},{'$set':{"check": "0"}})
			return render_template('box4updating.html', show_name=dept, show_dept=fullname, namelist=namelist, 
			keynamelist=keynamelist, compnamelist=compnamelist, monthlist=monthlist, daylist=daylist, 
			hourlist=hourlist, minutelist=minutelist, keycolorlist =keycolorlist, nokeycolorlist=nokeycolorlist, firstkeylist=firstkeylist, 
			secondkeylist=secondkeylist,Error_code=zebradata,RPIError_code=rpierror)

		time.sleep(5.5)


		mystatecollection.update_one({"user_id": 4},{'$set':{"state": "0"}})

	#html list
	ukeylist       = get_list.tempkey_list(4)
	unamelist      = get_list.name_list(4)
	ucompnamelist  = get_list.compname_list(4)
	umonthlist     = get_list.month_list(4)
	udaylist       = get_list.day_list(4)
	uhourlist      = get_list.hour_list(4)
	uminutelist    = get_list.minute_list(4)
	ukeycolorlist  = get_list.keycolor_list(4)
	unokeycolorlist  = get_list.nokeycolor_list(4)

	#greenred
	for doc_rpidata in findRpiData:
		rpidata=doc_rpidata["rpistatus"]

	for eror_code in findZebraData:
		zebradata=eror_code["Error_code"]
		# logger_1.info(zebradata) 

	for rpi_code in findRPIError:
		rpierror=rpi_code["RPIError_code"]	

	return render_template('box4.html', show_name=dept, show_dept=fullname, namelist=unamelist,  rpi=rpidata,
	compnamelist=ucompnamelist, monthlist=umonthlist, daylist=udaylist, hourlist=uhourlist, keynamelist=keynamelist, 
	minutelist=uminutelist, keycolorlist=ukeycolorlist, nokeycolorlist=unokeycolorlist, firstkeylist=firstkeylist, secondkeylist=ukeylist,Error_code=zebradata,RPIError_code=rpierror)




@app.route('/registration', methods=['GET', 'POST'])
def registration():
	logger_1.info('Registration Page...')
	box_no = 1
	keynamelist, keyIdlist, keyboxlist, keycolorlist, nokeycolorlist = ([] for i in range(5))
	indexlist, rentcomplist, rentcompidlist, btnlist = ([] for i in range(4))

	if request.method == 'POST':
		box_no = request.form['box']
		logger_1.info('User Selected Box' + box_no +'...')

	mycheckboxcollection.update_one({"user_id": 1},{'$set':{"box": box_no}})
	findKeyName = mykeynamecollection.find(filter = { "user_id" : int(box_no)})
	findKeyId = mykeyIdcollection.find(filter = { "user_id" : int(box_no)})
	findKeyBoxId = mykeyboxcollection.find(filter = { "user_id" : int(box_no)})
	findRentalComp = myrentalcompanycollection.find(filter = { "user_id" : int(box_no)})
	findRentalCompId = myrentalcompanyidcollection.find(filter = { "user_id" : int(box_no)})
	findKeyColor = mykeycolorcollection.find(filter = { "user_id" : int(box_no)})
	findNoKeyColor = mynokeycolorcollection.find(filter = { "user_id" : int(box_no)})

	for doc_keyname in findKeyName:
		for i in range(1,101):
			keynamelist.insert(i-1,doc_keyname["keyname%i" %i])

	for doc_keyId in findKeyId:
		for i in range(1,101):
			keyIdlist.insert(i-1,doc_keyId["keyId%i" %i])

	for doc_keybox in findKeyBoxId:
		for i in range(1,101):
			keyboxlist.insert(i-1,doc_keybox["keybox%i" %i])

	for doc_rentcomp in findRentalComp:
		for i in range(1,101):
			rentcomplist.insert(i-1,doc_rentcomp["rentcomp%i" %i])

	for doc_rentcompid in findRentalCompId:
		for i in range(1,101):
			rentcompidlist.insert(i-1,doc_rentcompid["rentcompid%i" %i])

	for doc_epckeycolor in findKeyColor:
		for i in range(1,101):
			keycolorlist.insert(i-1,doc_epckeycolor["keycolor%i" %i])

	for doc_epcnokeycolor in findNoKeyColor:
		for i in range(1,101):
			nokeycolorlist.insert(i-1,doc_epcnokeycolor["keycolor%i" %i])

	for i in range(1,101):
		btnlist.insert(i-1,"")

	logger_1.info('Generating table for Box' + str(box_no) +'...')
	record_df = pd.DataFrame({'btn': btnlist[:100], 'キーボックス番号': keyboxlist[:100], '従業員名': keynamelist[:100], 'タグID': keyIdlist[:100], 'レンタル会社': rentcomplist, 'レンタル会社 管理番号': rentcompidlist, '返却色': keycolorlist, '貸出色': nokeycolorlist})
	record_sys = pd.DataFrame()
	record_syscopy = pd.DataFrame()
	record_df.index = record_df.index + 1
	record_sys = record_df
	#copying dataframe and making a excel file
	export_excel = record_sys.to_csv (r'C:\\Face\\Test\\Record_Table.csv', index = True, header=True,encoding="utf-16", mode = 'w')
	#reading that excel file
	df = pd.read_csv(r'C:\\Face\\Test\\Record_Table.csv', encoding="utf-16")
	#Replacing Nan values in button column into 修正
	df3 = df.replace(np.nan, '修正', regex=True)
	#Removing the btn column
	df_new = df3.rename(columns={'btn': ''})
	#Renaming the key name column
	df2 = df_new.rename(columns={'従業員名': 'キー名'})
	#Removing all the column name  "Unnamed"   
	df1=df2.loc[:, ~df.columns.str.match('Unnamed')]
	#Increasing the index count by 1 
	df1.index = df1.index + 1
	#Renaming the index column with "No."
	df1.index.name = 'No.'
	# print(str(box_no)) 
	no=str(box_no)
	# print(no)
	current_date=datetime.now()
	current_time=current_date.strftime("%m_%d_%H_%M_%S")
	# print(current_time)
	filename1="C:\\record\\BoxRecord1_" + str(current_time)
	filename2="C:\\record\\BoxRecord2_" + str(current_time)
	filename3="C:\\record\\BoxRecord3_" + str(current_time)
	filename4="C:\\record\\BoxRecord4_" + str(current_time)
	if no == "1":
		export_excel = df1.to_excel(str((filename1 + '.xlsx')))
	elif no =="2":
		export_excel = df1.to_excel(str((filename2 + '.xlsx')))
	elif no == "3":
		export_excel = df1.to_excel(str((filename3 + '.xlsx')))
	elif no == "4":
		export_excel = df1.to_excel(str((filename4 + '.xlsx')))	
	


	for i in record_df.index:
		indexlist.append(str(i))
		
	record_df.insert(0, "", indexlist, True)
	# print(record_df)
	sendtabledata = record_df.to_dict(orient='records')
	# print(sendtabledata)
	logger_1.info('Sending Box' + str(box_no) +' table to HTML Page...')

	return render_template("registration.html",  tabledata=sendtabledata)

@app.route('/modify_data', methods=['GET', 'POST'])
def modify_data():
	checkbox = 1
	keynamelist, keyIdlist, keyboxlist, keycolorlist, nokeycolorlist = ([] for i in range(5))
	indexlist, rentcomplist, rentcompidlist, btnlist = ([] for i in range(4))

	findBox = mycheckboxcollection.find()
	for doc_checkbox in findBox:
		checkbox = doc_checkbox["box"]

	if request.method == 'POST':
		updated_keyname = request.form['keyID']
		updated_tagid = request.form['タグID']
		# updated_keybox = request.form['キーボックス']
		updated_rentcomp = request.form['rentcomp']
		updated_rentcompid = request.form['rentcompid']
		updated_keycolor = request.form['key_color']
		number = request.form['submit']
		num = int(number)
		logger_1.info('Updating the database of Key' + number + ' of Box' + str(checkbox) + '...')
		if updated_rentcomp=="" or updated_rentcompid=="":
			updated_rentcomp=" "
		if updated_rentcompid=="":
			updated_rentcompid=" "
		for i in range(1,101):
			if i == num:
				mykeynamecollection.update_one({"user_id": int(checkbox)},{'$set':{"keyname%i" %i:updated_keyname}})
				mykeyIdcollection.update_one({"user_id": int(checkbox)},{'$set':{"keyId%i" %i:updated_tagid}})
				myrentalcompanycollection.update_one({"user_id": int(checkbox)},{'$set':{"rentcomp%i" %i:updated_rentcomp}})
				myrentalcompanyidcollection.update_one({"user_id": int(checkbox)},{'$set':{"rentcompid%i" %i:updated_rentcompid}})
				mykeycolorcollection.update_one({"user_id": int(checkbox)},{'$set':{"keycolor%i" %i:updated_keycolor}})

	findKeyName = mykeynamecollection.find(filter = { "user_id" : int(checkbox)})
	findKeyId = mykeyIdcollection.find(filter = { "user_id" : int(checkbox)})
	findKeyBoxId = mykeyboxcollection.find(filter = { "user_id" : int(checkbox)})
	findRentalComp = myrentalcompanycollection.find(filter = { "user_id" : int(checkbox)})
	findRentalCompId = myrentalcompanyidcollection.find(filter = { "user_id" : int(checkbox)})
	findKeyColor = mykeycolorcollection.find(filter = { "user_id" : int(checkbox)})
	findNoKeyColor = mynokeycolorcollection.find(filter = { "user_id" : int(checkbox)})

	for doc_keyname in findKeyName:
		for i in range(1,101):
			keynamelist.insert(i-1,doc_keyname["keyname%i" %i])

	for doc_keyId in findKeyId:
		for i in range(1,101):
			keyIdlist.insert(i-1,doc_keyId["keyId%i" %i])

	for doc_keybox in findKeyBoxId:
		for i in range(1,101):
			keyboxlist.insert(i-1,doc_keybox["keybox%i" %i])

	for doc_rentcomp in findRentalComp:
		for i in range(1,101):
			rentcomplist.insert(i-1,doc_rentcomp["rentcomp%i" %i])

	for doc_rentcompid in findRentalCompId:
		for i in range(1,101):
			rentcompidlist.insert(i-1,doc_rentcompid["rentcompid%i" %i])

	for doc_epckeycolor in findKeyColor:
		for i in range(1,101):
			keycolorlist.insert(i-1,doc_epckeycolor["keycolor%i" %i])

	for doc_epcnokeycolor in findNoKeyColor:
		for i in range(1,101):
			nokeycolorlist.insert(i-1,doc_epcnokeycolor["keycolor%i" %i])

	for i in range(1,101):
		btnlist.insert(i-1,"")

	logger_1.info('Generating table for Box' + str(checkbox) +'...')
	record_df = pd.DataFrame({'btn': btnlist[:100], 'キーボックス番号': keyboxlist[:100], '従業員名': keynamelist[:100], 'タグID': keyIdlist[:100], 'レンタル会社': rentcomplist, 'レンタル会社 管理番号': rentcompidlist, '返却色': keycolorlist, '貸出色': nokeycolorlist})
	record_df.index = record_df.index + 1
	for i in record_df.index:
		indexlist.append(str(i))
	record_df.insert(0, "", indexlist, True)
	sendtabledata = record_df.to_dict(orient='records')
	logger_1.info('Sending Box' + str(checkbox) +' table to HTML Page...')

	return render_template("registration.html",  tabledata=sendtabledata)

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	checkbox = 1
	keynamelist, keyIdlist, keyboxlist, keycolorlist, nokeycolorlist = ([] for i in range(5))
	indexlist, rentcomplist, rentcompidlist, btnlist, keycolor_list, nokeycolor_list = ([] for i in range(6))
	html_taglist, keybox_list, key_list, rentcomp_list, rentcompid_list = ([] for i in range(5))

	findBox = mycheckboxcollection.find()
	for doc_checkbox in findBox:
		checkbox = doc_checkbox["box"]

	if request.method == 'POST':
		f = request.files['csv_file']
		logger_1.info('User has Uploaded a csv file: ' + f.filename + '...')
		f.save(f.filename)
		m=f.filename
		df=pd.DataFrame()
		try:
		
			if m.endswith('.xlsx'):
				uploaded_df = pd.read_excel (f.filename)
				# print(uploaded_df)
				
			elif m.endswith('.csv'):
					uploaded_df= pd.read_csv(f.filename)

					# print(uploaded_df)
		except Exception as e:
			print(e)			
			
		df = uploaded_df.replace(np.nan, '-', regex=True)
		# print(df)			
		for r in df["キーボックス番号"]:
			keybox_list.append(r)
		for r in df["キー名"]:
			key_list.append(r)
		for r in df["タグID"]:
			html_taglist.append(r)
		for r in df["レンタル会社"]:
			rentcomp_list.append(r)
		for r in df["レンタル会社 管理番号"]:
			rentcompid_list.append(r)
		for r in df["返却色"]:
			keycolor_list.append(r)
		for r in df["貸出色"]:
			nokeycolor_list.append(r)

		logger_1.info('Updating the database...')

		for i in range(1,101):
			mykeynamecollection.update_one({"user_id": int(checkbox)},{'$set':{"keyname%i" %i:key_list[i-1]}})
			mykeyIdcollection.update_one({"user_id": int(checkbox)},{'$set':{"keyId%i" %i:html_taglist[i-1]}})
			mykeyboxcollection.update_one({"user_id": int(checkbox)},{'$set':{"keybox%i" %i:keybox_list[i-1]}})
			myrentalcompanycollection.update_one({"user_id": int(checkbox)},{'$set':{"rentcomp%i" %i:rentcomp_list[i-1]}})
			myrentalcompanyidcollection.update_one({"user_id": int(checkbox)},{'$set':{"rentcompid%i" %i:rentcompid_list[i-1]}})
			mykeycolorcollection.update_one({"user_id": int(checkbox)},{'$set':{"keycolor%i" %i:keycolor_list[i-1]}})
			mynokeycolorcollection.update_one({"user_id": int(checkbox)},{'$set':{"keycolor%i" %i:nokeycolor_list[i-1]}})

	findKeyName = mykeynamecollection.find(filter = { "user_id" : int(checkbox)})
	findKeyId = mykeyIdcollection.find(filter = { "user_id" : int(checkbox)})
	findKeyBoxId = mykeyboxcollection.find(filter = { "user_id" : int(checkbox)})
	findRentalComp = myrentalcompanycollection.find(filter = { "user_id" : int(checkbox)})
	findRentalCompId = myrentalcompanyidcollection.find(filter = { "user_id" : int(checkbox)})
	findKeyColor = mykeycolorcollection.find(filter = { "user_id" : int(checkbox)})
	findNoKeyColor = mynokeycolorcollection.find(filter = { "user_id" : int(checkbox)})

	for doc_keyname in findKeyName:
		for i in range(1,101):
			keynamelist.insert(i-1,doc_keyname["keyname%i" %i])

	for doc_keyId in findKeyId:
		for i in range(1,101):
			keyIdlist.insert(i-1,doc_keyId["keyId%i" %i])

	for doc_keybox in findKeyBoxId:
		for i in range(1,101):
			keyboxlist.insert(i-1,doc_keybox["keybox%i" %i])

	for doc_rentcomp in findRentalComp:
		for i in range(1,101):
			rentcomplist.insert(i-1,doc_rentcomp["rentcomp%i" %i])

	for doc_rentcompid in findRentalCompId:
		for i in range(1,101):
			rentcompidlist.insert(i-1,doc_rentcompid["rentcompid%i" %i])

	for doc_epckeycolor in findKeyColor:
		for i in range(1,101):
			keycolorlist.insert(i-1,doc_epckeycolor["keycolor%i" %i])

	for doc_epcnokeycolor in findNoKeyColor:
		for i in range(1,101):
			nokeycolorlist.insert(i-1,doc_epcnokeycolor["keycolor%i" %i])

	for i in range(1,101):
		btnlist.insert(i-1,"")

	logger_1.info('Generating table for Box' + str(checkbox) +'...')
	record_df = pd.DataFrame({'btn': btnlist[:100], 'キーボックス番号': keyboxlist[:100], '従業員名': keynamelist[:100], 'タグID': keyIdlist[:100], 'レンタル会社': rentcomplist, 'レンタル会社 管理番号': rentcompidlist, '返却色': keycolorlist, '貸出色': nokeycolorlist})
	record_df.index = record_df.index + 1
	for i in record_df.index:
		indexlist.append(str(i))
	record_df.insert(0, "", indexlist, True)
	sendtabledata = record_df.to_dict(orient='records')
	# print(sendtabledata)
	logger_1.info('Sending Box' + str(checkbox) +' table to HTML Page...')

	return render_template("registration.html",  tabledata=sendtabledata)

@app.route('/pdfdownload')
def pdfdownload():
	try:
		box_no = 1

		findBox = mycheckboxcollection.find()
		for doc_checkbox in findBox:
			box_no = doc_checkbox["box"]

		get_pdf.return_pdf(str(box_no))
		logger_1.info('Key Info PDF file for box ' + str(box_no) +' has been downloaded...')

		return send_file('C:\\Face\\pdf\\KeyInfo.pdf', attachment_filename='KeyInfo.pdf', as_attachment=True)
	except Exception as e:
		logger_1.error('Error has occurred in downloading Key Info PDF file for box ' + str(box_no) +'...')
		return str(e)


		
@ app.route ('/userinputrecord', methods=['GET', 'POST']) 
def  userinputrecord():
	# logger_1.info('User Selected Record Page...')
	keynamelist, indexlist, numberlist, uin = ([] for i in range(4))
	keybox = check = 1

	try:
		if request.method == 'POST':
			info = request.form.getlist('info')
			# print(info)
			if len(info) > 0:
				uin = info
				logger_1.info(uin)

			try:
				updated_compname = request.form['data1']
				updated_username = request.form['data2']
				updated_keyname = request.form['data3']
				updated_dateTime = request.form['data4']
				logger_1.info(updated_compname)
				logger_1.info(updated_username)
				logger_1.info(updated_keyname)
				logger_1.info(updated_dateTime)
				for i in range(1,16):
					collname = "RecordDatabase" + str(i)
					myrecordcollection = mydb[collname]
					myrecordcollection.update_one({"時刻": updated_dateTime, "キー名": updated_keyname},
					{'$set':{"部署名": updated_compname, "貸出者": updated_username}})
				
				keybox = request.form['data5']
				if keybox == "キーボックス 1":
					keybox = 1
				if keybox == "キーボックス 2":
					keybox = 2
				if keybox == "キーボックス 3":
					keybox = 3
				if keybox == "キーボックス 4":
					keybox = 4	
				logger_1.info(keybox)
				for i in range(1,10):
					keynameNo = "00" + str(i)
					findKeyName = mykeynamecollection.find(filter = { "user_id" : keybox})
					for doc_keyname in findKeyName:
						keynamevalue = doc_keyname["keyname%i" %i]
						if keynamevalue == updated_keyname or keynameNo in updated_keyname:
							check = i 
							break
				for i in range(10,100):
					keynameNo = "0" + str(i)
					findKeyName = mykeynamecollection.find(filter = { "user_id" : keybox})
					for doc_keyname in findKeyName:
						keynamevalue = doc_keyname["keyname%i" %i]
						if keynamevalue == updated_keyname or keynameNo in updated_keyname:
							check = i 
							break
				keynameNo = "100"
				if keynameNo in updated_keyname:
					findKeyName = mykeynamecollection.find(filter = { "user_id" : keybox})
					for doc_keyname in findKeyName:
						keynamevalue = doc_keyname["keyname%i" %i]
						if keynamevalue == updated_keyname:
							check = i 
							break
				nametofix = "name" + str(check)
				logger_1.info(nametofix)
				comptofix = "dept" + str(check)
				logger_1.info(comptofix)
				mynamecollection.update_one({"user_id": keybox},{'$set':{nametofix: updated_username[0:4]}})
				mydeptcollection.update_one({"user_id": keybox},{'$set':{comptofix: updated_compname}})
			except Exception as e:
				logger_1.error(e)

		findKeyName = mykeynamecollection.find(filter = { "user_id" : 1})
		findKeyId = mykeyIdcollection.find()

		for doc_keyname in findKeyName:
			for i in range(1,101):
				keynamelist.insert(i-1,doc_keyname["keyname%i" %i])

		for i in range(1,101):
			numberlist.append(str(i))

		# logger_1.info('Generating record table...')

		record_showlist = get_recordshowdata.output_list(uin, numberlist)
		# print(record_showlist)
		record_df = get_record.output_df(uin, keynamelist, numberlist, str(date.today()))
		# print(record_df)
		



		df_length = len(record_df)
		for i in range(1,df_length+1):
			indexlist.append(str(i))
		record_df.insert(0, "", indexlist, True)
		send_data = record_df.to_dict(orient='records')
		keynamelist = json.dumps(keynamelist)
		numberlist = json.dumps(numberlist)
		uin = json.dumps(uin)

		# logger_1.info('Sending record table to HTML Page...')
	except Exception as e:
		logger_1.error(e)
	# return render_template('view.html',tables=[record_df.to_html(classes='record_df')],titles = ['na', 'RECORD' ])
	return render_template ('record.html', data_list=send_data, numberlist=numberlist, showlist=record_showlist, uinlist=uin)



@app.route('/login', methods=['GET', 'POST'])
def login():	
	error = None
	if request.method == 'POST':
		if request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
			logger_1.error('Wrong Password for Management Page...')
		else:
			logger_1.info('Admin logged into Management Page...')
			return redirect(url_for('kanri'))
	return render_template('login.html', error=error)

@app.route('/kanri')
def kanri():
	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list()
	part6list = get_kanrilist.part6_list()

	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list, part5list=part5list,part6list=part6list)

@app.route('/kanripart2', methods=['GET', 'POST'])
def kanripart2():
	mycheckdaycollection = mydb["CheckUserInputDays"]
	if request.method == 'POST':
		hour = request.form['hour']
		minute = request.form['minute']
		daynum = request.form['howmanydays']
		mykanripart2savehourcollection.update_one({"user_id": 1},{'$set':{"hour": hour}})
		mykanripart2saveminutecollection.update_one({"user_id": 1},{'$set':{"minute": minute}})
		mycheckdaycollection.update_one({"user_id": 1},{'$set':{"daynum": daynum}})

		mail1 = request.form['mail5']
		mail2 = request.form['mail6']
		mail3 = request.form['mail7']
		mail4 = request.form['mail8']
		mykeynotreturnemailcollection.update_one({"user_id": 1},{'$set':{"email1": mail1}})
		mykeynotreturnemailcollection.update_one({"user_id": 1},{'$set':{"email2": mail2}})
		mykeynotreturnemailcollection.update_one({"user_id": 1},{'$set':{"email3": mail3}})
		mykeynotreturnemailcollection.update_one({"user_id": 1},{'$set':{"email4": mail4}})

	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list() #for changing the system IP Address
	part6list = get_kanrilist.part6_list()
	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list,part5list=part5list,part6list=part6list)

@app.route('/kanripart3', methods=['GET', 'POST'])
def kanripart3():
	mykanripart3dbcollection = mydb["KanriPart3DB"]
	if request.method == 'POST':
		secondnum = request.form['howmanyseconds']
		mykanripart3dbcollection.update_one({"user_id": 1},{'$set':{"seconds": int(secondnum)}})
	
	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list()
	part6list = get_kanrilist.part6_list()
	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list,part5list=part5list,part6list=part6list)
#to update ip of the system
@app.route('/kanripart5', methods=['GET', 'POST'])
def kanripart5():
	mysysipdatadbcollection = mydb["SYSIPData"]
	# myipdatadbcollection = mydb["IPData"]

	if request.method == 'POST':
		newsystemip = request.form['SYSIPData']
		# print(newsystemip)
		logger_1.info("Admin logged in admin Page and updated the id as below..")
		mysysipdatadbcollection.update_one({"user_id": 1},{'$set':{"sysip_address": str(newsystemip)}})
		logger_1.info(newsystemip)
		# myipdatadbcollection.update_one({"user_id": 1},{'$set':{"ip_address": str(newPIip)}})

	
	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list()
	part6list = get_kanrilist.part6_list()
	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list,part5list=part5list,part6list=part6list)

@app.route('/kanripart6', methods=['GET', 'POST'])
def kanripart6():
	if request.method == 'POST':
		mode = request.form['mode']
		myfacemodecollection.update_one({"user_id": 1},{'$set':{"mode": mode}})
	
	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list()
	part6list = get_kanrilist.part6_list()
	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list, part5list=part5list,part6list=part6list)
@app.route('/saverecordinfo', methods=['GET', 'POST'])
def saverecordinfo():
	if request.method == 'POST':
		day = request.form['day']
		hour = request.form['hour']
		minute = request.form['minute']
		if day != "" and hour != "" and minute != "":
			mysavedaycollection.update_one({"user_id": 1},{'$set':{"day": int(day)}})
			mysavehourcollection.update_one({"user_id": 1},{'$set':{"hour": hour}})
			mysaveminutecollection.update_one({"user_id": 1},{'$set':{"minute": minute}})

		mail1 = request.form['mail1']
		mail2 = request.form['mail2']
		mail3 = request.form['mail3']
		mail4 = request.form['mail4']
		mymonthlysaveemailcollection.update_one({"user_id": 1},{'$set':{"email1": mail1}})
		mymonthlysaveemailcollection.update_one({"user_id": 1},{'$set':{"email2": mail2}})
		mymonthlysaveemailcollection.update_one({"user_id": 1},{'$set':{"email3": mail3}})
		mymonthlysaveemailcollection.update_one({"user_id": 1},{'$set':{"email4": mail4}})
	
	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list()

	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list, part5list=part5list)

@app.route('/antennainfo', methods=['GET', 'POST'])
def antennainfo():
	uin = []
	antennalist = []

	mydb2 = myclient['box2project']
	mysignalb1collection = mydb2["SignalDataB1"]
	mysignalb2collection = mydb2["SignalDataB2"]
	mysignalb3collection = mydb2["SignalDataB3"]
	mysignalb4collection = mydb2["SignalDataB4"]
	myantennab1collection = mydb2["AntennaDataB1"]
	myantennab2collection = mydb2["AntennaDataB2"]
	myantennab3collection = mydb2["AntennaDataB3"]
	myantennab4collection = mydb2["AntennaDataB4"]

	if request.method == 'POST':
		uin = request.form.getlist('info')
		logger_1.info('Admin modified Antenna Number of Boxes...')
		logger_1.info(uin)
	
	for a in uin:
		for i in range(1,9):
			if a=="a%ib1" %i:
				antennalist.append(str(i))
				myantennab1collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
			if a=="a%ib2" %i:
				antennalist.append(str(i))
				myantennab2collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
			if a=="a%ib3" %i:
				antennalist.append(str(i))
				myantennab3collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
			if a=="a%ib4" %i:
				antennalist.append(str(i))
				myantennab4collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
	
	#html list
	part1list = get_kanrilist.part1_list()
	part2list = get_kanrilist.part2_list()
	part3list = get_kanrilist.part3_list()
	part4list = get_kanrilist.part4_list()
	part5list = get_kanrilist.part5_list()

	return render_template('kanri.html', part1list=part1list, part2list=part2list, part3list=part3list, part4list=part4list, part5list=part5list)

@ app.route ('/graphmenu', methods=['GET', 'POST']) 
def  graphmenu():
	logger_1.info('User Selected GraphMenu Page...')
	global uin
	uin = []
	keynamelist, keyIdlist, indexlist, filterlist = ([] for i in range(4))
	datedb_list, dates = ([] for i in range(2))

	if request.method == 'POST':
		uin = request.form.getlist('info')
		logger_1.info(uin)

		if uin[3] == "dategraph":
			logger_1.info('User Selected DateTime Graph...')
			logger_1.info('Sending Graph Figure to HTML Page...')
			src = get_graph.dategraph(uin)
			return render_template('dategraph.html', url=src)
		if uin[3] == "keynamegraph":
			logger_1.info('User Selected KeyName Graph...')
			logger_1.info('Sending Graph Figure to HTML Page...')
			src = get_graph.keynamegraph(uin)
			return render_template('keynamegraph.html', url=src)
		if uin[3] == "compnamegraph":
			logger_1.info('User Selected CompanyName Graph...')
			logger_1.info('Sending Graph Figure to HTML Page...')
			src = get_graph.compnamegraph(uin)
			return render_template('compnamegraph.html', url=src)

	return render_template ('graphmenu.html')

##############################################     API     #############################################
@app.route('/user_input', methods=['GET', 'POST'])
def user_input():
	logger_1.info('Manual Page for fixing Antenna Numbers...')
	
	mydb2 = myclient['box2project']
	mysignalb1collection = mydb2["SignalDataB1"]
	mysignalb2collection = mydb2["SignalDataB2"]
	mysignalb3collection = mydb2["SignalDataB3"]
	mysignalb4collection = mydb2["SignalDataB4"]
	myantennab1collection = mydb2["AntennaDataB1"]
	myantennab2collection = mydb2["AntennaDataB2"]
	myantennab3collection = mydb2["AntennaDataB3"]
	myantennab4collection = mydb2["AntennaDataB4"]

	uin = []
	antennalist = []
	if request.method == 'POST':
		uin = request.form.getlist('info')
		logger_1.info(uin)

		for i in uin:
			if i=="yb1":
				mysignalb1collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
				break
			else:
				mysignalb1collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
		for i in uin:
			if i=="yb2":
				mysignalb2collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
				break
			else:
				mysignalb2collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
		for i in uin:
			if i=="yb3":
				mysignalb3collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
				print(i)
				break
			else:
				mysignalb3collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
		for i in uin:
			if i=="yb4":
				mysignalb4collection.update_one({"user_id": 1},{'$set':{"signal": "Start"}})
				break
			else:
				mysignalb4collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
		for i in uin:
			if i=="nb1":
				mysignalb1collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
				break
		for i in uin:
			if i=="nb2":
				mysignalb2collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
				break
		for i in uin:
			if i=="nb3":
				mysignalb3collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
				break
		for i in uin:
			if i=="nb4":
				mysignalb4collection.update_one({"user_id": 1},{'$set':{"signal": "Stop"}})
				break
		for a in uin:
			for i in range(1,9):
				# print(a)
				if a=="a%ib1" %i:
					antennalist.append(str(i))
					logger_1.info(antennalist)
					myantennab1collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
				if a=="a%ib2" %i:
					antennalist.append(str(i))
					logger_1.info(antennalist)
					myantennab2collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
				if a=="a%ib3" %i:
					antennalist.append(str(i))
					logger_1.info(antennalist)
					myantennab3collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
				if a=="a%ib4" %i:
					antennalist.append(str(i))
					logger_1.info(antennalist)
					myantennab4collection.update_one({"user_id": 1},{'$set':{"antennaA": antennalist[len(antennalist)-2], "antennaB": antennalist[len(antennalist)-1]}})
	return render_template('apimain.html')

@app.route('/data/<string:box>', methods=['GET'])
def returnOne(box):
	logger_1.info('API Page Displaying the Specific Antenna Numbers for Specific Box...')
	
	mydb2 = myclient['box2project']
	mysignalb1collection = mydb2["SignalDataB1"]
	mysignalb2collection = mydb2["SignalDataB2"]
	mysignalb3collection = mydb2["SignalDataB3"]
	mysignalb4collection = mydb2["SignalDataB4"]
	myantennab1collection = mydb2["AntennaDataB1"]
	myantennab2collection = mydb2["AntennaDataB2"]
	myantennab3collection = mydb2["AntennaDataB3"]
	myantennab4collection = mydb2["AntennaDataB4"]

	findSignalB1 = mysignalb1collection.find(filter = { "user_id" : 1})
	findSignalB2 = mysignalb2collection.find(filter = { "user_id" : 1})
	findSignalB3 = mysignalb3collection.find(filter = { "user_id" : 1})
	findSignalB4 = mysignalb4collection.find(filter = { "user_id" : 1})

	for doc_signal in findSignalB1:
		globals()["data1"]=doc_signal["signal"]
	for doc_signal in findSignalB2:
		globals()["data2"]=doc_signal["signal"]
	for doc_signal in findSignalB3:
		globals()["data3"]=doc_signal["signal"]
	for doc_signal in findSignalB4:
		globals()["data4"]=doc_signal["signal"]

	findAntennaB1 = myantennab1collection.find()
	findAntennaB2 = myantennab2collection.find()
	findAntennaB3 = myantennab3collection.find()
	findAntennaB4 = myantennab4collection.find()

	for doc_antenna in findAntennaB1:
		globals()["antenna1"]=doc_antenna["antennaA"]
		globals()["antenna2"]=doc_antenna["antennaB"]
	for doc_antenna in findAntennaB2:
		globals()["antenna3"]=doc_antenna["antennaA"]
		globals()["antenna4"]=doc_antenna["antennaB"]
	for doc_antenna in findAntennaB3:
		globals()["antenna5"]=doc_antenna["antennaA"]
		globals()["antenna6"]=doc_antenna["antennaB"]
	for doc_antenna in findAntennaB4:
		globals()["antenna7"]=doc_antenna["antennaA"]
		globals()["antenna8"]=doc_antenna["antennaB"]

	send_data = [{'box': '1', 'check': data1, 'antennaA': antenna1, 'antennaB': antenna2},
				 {'box': '2', 'check': data2, 'antennaA': antenna3, 'antennaB': antenna4},
				 {'box': '3', 'check': data3, 'antennaA': antenna5, 'antennaB': antenna6},
				 {'box': '4', 'check': data4, 'antennaA': antenna7, 'antennaB': antenna8}]

	theOne = send_data[0]
	for i,q in enumerate(send_data):
		if q['box'] == box:
			theOne = send_data[i]
	return jsonify(theOne)

@app.route('/data', methods=['GET'])
def returnAll():
	mydb2 = myclient['box2project']
	mysignalb1collection = mydb2["SignalDataB1"]
	mysignalb2collection = mydb2["SignalDataB2"]
	mysignalb3collection = mydb2["SignalDataB3"]
	mysignalb4collection = mydb2["SignalDataB4"]
	myantennab1collection = mydb2["AntennaDataB1"]
	myantennab2collection = mydb2["AntennaDataB2"]
	myantennab3collection = mydb2["AntennaDataB3"]
	myantennab4collection = mydb2["AntennaDataB4"]

	findSignalB1 = mysignalb1collection.find(filter = { "user_id" : 1})
	findSignalB2 = mysignalb2collection.find(filter = { "user_id" : 1})
	findSignalB3 = mysignalb3collection.find(filter = { "user_id" : 1})
	findSignalB4 = mysignalb4collection.find(filter = { "user_id" : 1})

	for doc_signal in findSignalB1:
		globals()["data1"]=doc_signal["signal"]
	for doc_signal in findSignalB2:
		globals()["data2"]=doc_signal["signal"]
	for doc_signal in findSignalB3:
		globals()["data3"]=doc_signal["signal"]
	for doc_signal in findSignalB4:
		globals()["data4"]=doc_signal["signal"]

	findAntennaB1 = myantennab1collection.find()
	findAntennaB2 = myantennab2collection.find()
	findAntennaB3 = myantennab3collection.find()
	findAntennaB4 = myantennab4collection.find()

	for doc_antenna in findAntennaB1:
		globals()["antenna1"]=doc_antenna["antennaA"]
		globals()["antenna2"]=doc_antenna["antennaB"]
	for doc_antenna in findAntennaB2:
		globals()["antenna3"]=doc_antenna["antennaA"]
		globals()["antenna4"]=doc_antenna["antennaB"]
	for doc_antenna in findAntennaB3:
		globals()["antenna5"]=doc_antenna["antennaA"]
		globals()["antenna6"]=doc_antenna["antennaB"]
	for doc_antenna in findAntennaB4:
		globals()["antenna7"]=doc_antenna["antennaA"]
		globals()["antenna8"]=doc_antenna["antennaB"]

	send_data = [{'box': '1', 'check': data1, 'antennaA': antenna1, 'antennaB': antenna2},
				 {'box': '2', 'check': data2, 'antennaA': antenna3, 'antennaB': antenna4},
				 {'box': '3', 'check': data3, 'antennaA': antenna5, 'antennaB': antenna6},
				 {'box': '4', 'check': data4, 'antennaA': antenna7, 'antennaB': antenna8}]
	return jsonify(send_data)

###########################################################################################




def rpspberryPiRun():
	try:
		pid1 = os.getpid()
		mycheckzebrapiddbcollection.update_one({"user_id": 1},{'$set':{"pid": pid1}})
		# print(pid1)
		# print("PI")
		logger_1.info('Raspberry Pi Started...')

		s1 = rpirun.make_connection(12345)
		s2 = rpirun.make_connection(5000)

		rpirun.sendreceive(s1,s2)
		# print("pi run")
	except Exception as e:
		logger_1.info("Raspberry Pi Part Threading Error")
		logger_1.error(e)

def kanripart1Class():
	try:
		kanri_part1_sendEmailMonthly.part1()
	except Exception as e:
		logger_1.info("Kanri Part 1 Threading Error")
		logger_1.error(e)

def kanripart2Class():
	try:

		kanri_part2_run.part2()
	except Exception as e:
		logger_1.info("Kanri Part 2 Threading Error")
		logger_1.error(e)

def ZebraConnection():
	try:
		checkZebra.run()
		# box1.run()
		print("run zebra")
	except Exception as e:
		logger_1.info("ZEBRA Connection")
		logger_1.error(e)


def box1():
	while True:
		findInfo = myinfocollection.find(filter = { "user_id" : 1})
		Room=[]
		for doc_info in findInfo:
			fullname=doc_info["fullname"]
			name=doc_info["name"]
			dept_name=doc_info["dept_name"]
			dept=doc_info["dept"]
			dday=doc_info["dday"]
			date_only=doc_info["date_only"]
			d_month=doc_info["d_month"]
			d_day=doc_info["d_day"]
			d_hour=doc_info["d_hour"]
			d_min=doc_info["d_min"]
			d_sec=doc_info["d_sec"]
			currsecond=d_sec

		#Assign individual variable to Take Out the Data from each Database Collection
		# print("inside 3 part1")
		findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 1})
		findState = mystatecollection.find(filter = { "user_id" : 1})
		findCheck = mycheckcollection.find(filter = { "user_id" : 1})
		findCondition = myconditioncollection.find(filter = { "user_id" : 1})
		findRpiData = myrpidatadbcollection.find()
		findZebraData = myzebraalertcollection.find()
		findRPIError  = myrpicheckalertcollection.find()


		#python list
		epckeylist     = get_list.epckey_list(1)
		epcnamelist    = get_list.epcname_list(1)
		epckeyboxlist  = get_list.epckeybox_list(1)
		keyidlist      = get_list.keyid_list(1)
		rentcomplist   = get_list.rentcomp_list(1)
		rentcompidlist = get_list.rentcompid_list(1)
		roomidlist     = get_list.roomid_list(1)

		#html list
		keynamelist   = get_list.keyname_list(1)
		namelist      = get_list.name_list(1)
		compnamelist  = get_list.compname_list(1)
		monthlist     = get_list.month_list(1)
		daylist       = get_list.day_list(1)
		hourlist      = get_list.hour_list(1)
		minutelist    = get_list.minute_list(1)
		keycolorlist  = get_list.keycolor_list(1)
		nokeycolorlist  = get_list.nokeycolor_list(1)
		firstkeylist  = get_list.key_list(1)
		secondkeylist = get_list.key_list(1)

		#condition variables
		# print("check 4")
		for doc_state in findState:
			state=doc_state["state"]

		for doc_check in findCheck:
			check=doc_check["check"]

		for doc_condition in findCondition:
			condition=doc_condition["condition"]

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]	

		if condition=="0":
			mycheckcollection.update_one({"user_id": 1},{'$set':{"check": "1"}})
			mystatecollection.update_one({"user_id": 1},{'$set':{"state": "1"}})
		
		if condition=="1" and state=="1":
			logger_1.info('Box1 has been opened...')
			if check=="1":
				logger_1.info('Checking the keys and Updating the Page...')
				mycheckcollection.update_one({"user_id": 1},{'$set':{"check": "0"}})
			
			time.sleep(5.5)
				
			
			try:
				logger_1.info('Reading \"test11.csv\"...')
				epcreader_df= pd.read_csv("C:\\Zebra\\test11.csv", engine='python')
				count1 = 0 
				
				for i in range(1,101):
					if keyidlist[i-1] in epcreader_df.values:
						number=epcreader_df[epcreader_df['EPCID'] == keyidlist[i-1]].index[0]
						datacount = int(epcreader_df["Count"][number])
						mytempepccountcollection.update_one({"user_id": 1},{'$set':{"epccount%i" %i:datacount}})
					elif keyidlist[i-1] not in epcreader_df.values:
						if keyidlist[i-1] == "-" or epcnamelist[i-1] == "-":
							mytempepccountcollection.update_one({"user_id": 1},{'$set':{"epccount%i" %i:1}})
						else:
							mytempepccountcollection.update_one({"user_id": 1},{'$set':{"epccount%i" %i:0}})
					if keyidlist[i-1] == "-":
						mytempepccountcollection.update_one({"user_id": 1},{'$set':{"epccount%i" %i:1}})

				for doc_tempepccount in findTempEPCCount:
					for i in range(1,101):
						globals()["tempepccount" + str(i)]=doc_tempepccount["epccount%i" %i]

				for i in range(1,101):
					if globals()["tempepccount" + str(i)]>abs(0):
						myTempKeycollection.update_one({"user_id": 1},{'$set':{"Tag%i" %i:1}})
						count1 = count1+1
					else:
						myTempKeycollection.update_one({"user_id": 1},{'$set':{"Tag%i" %i:0}})
				tempepckeylist = get_list.tempepckey_list(1)
				key_name_identifier,status_identifier, id_identifier, indexlist,usr_name_identifier = ([] for i in range(5))
				for i in range(1,101):
					if epckeylist[i-1] != tempepckeylist[i-1]:
						if tempepckeylist[i-1] == 1:
							myKeycollection.update_one({"user_id": 1},{'$set':{"Tag%i" %i:1}})
							df = pd.DataFrame(data = {"user_id": 1, "日付" : str(date_only),"時刻" : str(dday), '状況' : "返却", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							x=myrecordcollection.insert_many(df.to_dict('records'))
							print(df)
							
						else:
							myKeycollection.update_one({"user_id": 1},{'$set':{"Tag%i" %i:0}})
							mynamecollection.update_one({"user_id": 1},{'$set':{"name%i"  %i:name}})
							mydaycollection.update_one({"user_id": 1},{'$set':{"day%i" %i:d_day}})
							mymonthcollection.update_one({"user_id": 1},{'$set':{"month%i"  %i:d_month}})
							myhourcollection.update_one({"user_id": 1},{'$set':{"hour%i"  %i:d_hour}})
							myminutecollection.update_one({"user_id": 1},{'$set':{"minute%i"  %i:d_min}})
							mydeptcollection.update_one({"user_id": 1},{'$set':{"dept%i"  %i:dept_name}})
							df = pd.DataFrame(data = {"user_id": 1, "日付" : str(date_only),"時刻" : str(dday), '状況' : "貸出", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							print(df)
							x=myrecordcollection.insert_many(df.to_dict('records'))
						
			
			except:
				logger_1.error("EmptyDataError: No Columns to read from empty CSV file...")

			mystatecollection.update_one({"user_id": 1},{'$set':{"state": "0"}})

		

		#html list
		ukeylist       = get_list.tempkey_list(1)
		unamelist      = get_list.name_list(1)
		ucompnamelist  = get_list.compname_list(1)
		umonthlist     = get_list.month_list(1)
		udaylist       = get_list.day_list(1)
		uhourlist      = get_list.hour_list(1)
		uminutelist    = get_list.minute_list(1)
		ukeycolorlist  = get_list.keycolor_list(1)
		unokeycolorlist  = get_list.nokeycolor_list(1)

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]	


def box2():
	while True:
		findInfo = myinfocollection.find(filter = { "user_id" : 2})
		Room=[]
		for doc_info in findInfo:
			fullname=doc_info["fullname"]
			name=doc_info["name"]
			dept_name=doc_info["dept_name"]
			dept=doc_info["dept"]
			dday=doc_info["dday"]
			date_only=doc_info["date_only"]
			d_month=doc_info["d_month"]
			d_day=doc_info["d_day"]
			d_hour=doc_info["d_hour"]
			d_min=doc_info["d_min"]
			d_sec=doc_info["d_sec"]
			currsecond=d_sec

		#Assign individual variable to Take Out the Data from each Database Collection
		# print("inside 3 part1")
		findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 2})
		findState = mystatecollection.find(filter = { "user_id" : 2})
		findCheck = mycheckcollection.find(filter = { "user_id" : 2})
		findCondition = myconditioncollection.find(filter = { "user_id" : 2})
		findRpiData = myrpidatadbcollection.find()
		findZebraData = myzebraalertcollection.find()
		findRPIError  = myrpicheckalertcollection.find()


		#python list
		epckeylist     = get_list.epckey_list(2)
		epcnamelist    = get_list.epcname_list(2)
		epckeyboxlist  = get_list.epckeybox_list(2)
		keyidlist      = get_list.keyid_list(2)
		rentcomplist   = get_list.rentcomp_list(2)
		rentcompidlist = get_list.rentcompid_list(2)
		roomidlist     = get_list.roomid_list(2)

		#html list
		keynamelist   = get_list.keyname_list(2)
		namelist      = get_list.name_list(2)
		compnamelist  = get_list.compname_list(2)
		monthlist     = get_list.month_list(2)
		daylist       = get_list.day_list(2)
		hourlist      = get_list.hour_list(2)
		minutelist    = get_list.minute_list(2)
		keycolorlist  = get_list.keycolor_list(2)
		nokeycolorlist  = get_list.nokeycolor_list(2)
		firstkeylist  = get_list.key_list(2)
		secondkeylist = get_list.key_list(2)

		#condition variables
		# print("check 4")
		for doc_state in findState:
			state=doc_state["state"]

		for doc_check in findCheck:
			check=doc_check["check"]

		for doc_condition in findCondition:
			condition=doc_condition["condition"]

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]	

		if condition=="0":
			mycheckcollection.update_one({"user_id": 2},{'$set':{"check": "1"}})
			mystatecollection.update_one({"user_id": 2},{'$set':{"state": "1"}})
		
		if condition=="1" and state=="1":
			logger_1.info('Box2 has been opened...')
			if check=="1":
				logger_1.info('Checking the keys and Updating the Page...')
				mycheckcollection.update_one({"user_id": 2},{'$set':{"check": "0"}})
			
			time.sleep(5.5)
				
			
			try:
				logger_1.info('Reading \"test11.csv\"...')
				epcreader_df= pd.read_csv("C:\\Zebra\\test11.csv", engine='python')
				count1 = 0 
				
				for i in range(1,101):
					if keyidlist[i-1] in epcreader_df.values:
						number=epcreader_df[epcreader_df['EPCID'] == keyidlist[i-1]].index[0]
						datacount = int(epcreader_df["Count"][number])
						mytempepccountcollection.update_one({"user_id": 2},{'$set':{"epccount%i" %i:datacount}})
					elif keyidlist[i-1] not in epcreader_df.values:
						if keyidlist[i-1] == "-" or epcnamelist[i-1] == "-":
							mytempepccountcollection.update_one({"user_id": 2},{'$set':{"epccount%i" %i:1}})
						else:
							mytempepccountcollection.update_one({"user_id": 2},{'$set':{"epccount%i" %i:0}})
					if keyidlist[i-1] == "-":
						mytempepccountcollection.update_one({"user_id": 2},{'$set':{"epccount%i" %i:1}})

				for doc_tempepccount in findTempEPCCount:
					for i in range(1,101):
						globals()["tempepccount" + str(i)]=doc_tempepccount["epccount%i" %i]

				for i in range(1,101):
					if globals()["tempepccount" + str(i)]>abs(0):
						myTempKeycollection.update_one({"user_id": 2},{'$set':{"Tag%i" %i:1}})
						count1 = count1+1
					else:
						myTempKeycollection.update_one({"user_id": 2},{'$set':{"Tag%i" %i:0}})
				tempepckeylist = get_list.tempepckey_list(2)
				key_name_identifier,status_identifier, id_identifier, indexlist,usr_name_identifier = ([] for i in range(5))
				for i in range(1,101):
					if epckeylist[i-1] != tempepckeylist[i-1]:
						if tempepckeylist[i-1] == 1:
							myKeycollection.update_one({"user_id": 2},{'$set':{"Tag%i" %i:1}})
							df = pd.DataFrame(data = {"user_id": 2, "日付" : str(date_only),"時刻" : str(dday), '状況' : "返却", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							x=myrecordcollection.insert_many(df.to_dict('records'))
							print(df)
							
						else:
							myKeycollection.update_one({"user_id": 2},{'$set':{"Tag%i" %i:0}})
							mynamecollection.update_one({"user_id": 2},{'$set':{"name%i"  %i:name}})
							mydaycollection.update_one({"user_id": 2},{'$set':{"day%i" %i:d_day}})
							mymonthcollection.update_one({"user_id": 2},{'$set':{"month%i"  %i:d_month}})
							myhourcollection.update_one({"user_id": 2},{'$set':{"hour%i"  %i:d_hour}})
							myminutecollection.update_one({"user_id": 2},{'$set':{"minute%i"  %i:d_min}})
							mydeptcollection.update_one({"user_id": 2},{'$set':{"dept%i"  %i:dept_name}})
							df = pd.DataFrame(data = {"user_id": 2, "日付" : str(date_only),"時刻" : str(dday), '状況' : "貸出", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							print(df)
							x=myrecordcollection.insert_many(df.to_dict('records'))
						
			
			except:
				logger_1.error("EmptyDataError: No Columns to read from empty CSV file...")

			mystatecollection.update_one({"user_id": 2},{'$set':{"state": "0"}})

		

		#html list
		ukeylist       = get_list.tempkey_list(2)
		unamelist      = get_list.name_list(2)
		ucompnamelist  = get_list.compname_list(2)
		umonthlist     = get_list.month_list(2)
		udaylist       = get_list.day_list(2)
		uhourlist      = get_list.hour_list(2)
		uminutelist    = get_list.minute_list(2)
		ukeycolorlist  = get_list.keycolor_list(2)
		unokeycolorlist  = get_list.nokeycolor_list(2)

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]				

def box3():
	while True:
		flag=0
		findInfo = myinfocollection.find(filter = { "user_id" : 3})
		Room=[]
		for doc_info in findInfo:
			fullname=doc_info["fullname"]
			name=doc_info["name"]
			dept_name=doc_info["dept_name"]
			dept=doc_info["dept"]
			dday=doc_info["dday"]
			date_only=doc_info["date_only"]
			d_month=doc_info["d_month"]
			d_day=doc_info["d_day"]
			d_hour=doc_info["d_hour"]
			d_min=doc_info["d_min"]
			d_sec=doc_info["d_sec"]
			currsecond=d_sec

		#Assign individual variable to Take Out the Data from each Database Collection
		# print("inside 3 part1")
		findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 3})
		findState = mystatecollection.find(filter = { "user_id" : 3})
		findCheck = mycheckcollection.find(filter = { "user_id" : 3})
		findCondition = myconditioncollection.find(filter = { "user_id" : 3})
		findRpiData = myrpidatadbcollection.find()
		findZebraData = myzebraalertcollection.find()
		findRPIError  = myrpicheckalertcollection.find()


		#python list
		epckeylist     = get_list.epckey_list(3)
		epcnamelist    = get_list.epcname_list(3)
		epckeyboxlist  = get_list.epckeybox_list(3)
		keyidlist      = get_list.keyid_list(3)
		rentcomplist   = get_list.rentcomp_list(3)
		rentcompidlist = get_list.rentcompid_list(3)
		roomidlist     = get_list.roomid_list(3)

		#html list
		keynamelist   = get_list.keyname_list(3)
		namelist      = get_list.name_list(3)
		compnamelist  = get_list.compname_list(3)
		monthlist     = get_list.month_list(3)
		daylist       = get_list.day_list(3)
		hourlist      = get_list.hour_list(3)
		minutelist    = get_list.minute_list(3)
		keycolorlist  = get_list.keycolor_list(3)
		nokeycolorlist  = get_list.nokeycolor_list(3)
		firstkeylist  = get_list.key_list(3)
		secondkeylist = get_list.key_list(3)

		#condition variables
		# print("check 4")
		for doc_state in findState:
			state=doc_state["state"]

		for doc_check in findCheck:
			check=doc_check["check"]

		for doc_condition in findCondition:
			condition=doc_condition["condition"]

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]	

		if condition=="0":
			mycheckcollection.update_one({"user_id": 3},{'$set':{"check": "1"}})
			mystatecollection.update_one({"user_id": 3},{'$set':{"state": "1"}})
		
		if condition=="1" and state=="1":
			logger_1.info('Box3 has been opened...')
			if check=="1":
				logger_1.info('Checking the keys and Updating the Page...')
				mycheckcollection.update_one({"user_id": 3},{'$set':{"check": "0"}})
			
			time.sleep(5.5)
				
			
			try:
				logger_1.info('Reading \"test11.csv\"...')
				epcreader_df= pd.read_csv("C:\\Zebra\\test11.csv", engine='python')
				count1 = 0 
				
				for i in range(1,101):
					if keyidlist[i-1] in epcreader_df.values:
						number=epcreader_df[epcreader_df['EPCID'] == keyidlist[i-1]].index[0]
						datacount = int(epcreader_df["Count"][number])
						mytempepccountcollection.update_one({"user_id": 3},{'$set':{"epccount%i" %i:datacount}})
					elif keyidlist[i-1] not in epcreader_df.values:
						if keyidlist[i-1] == "-" or epcnamelist[i-1] == "-":
							mytempepccountcollection.update_one({"user_id": 3},{'$set':{"epccount%i" %i:1}})
						else:
							mytempepccountcollection.update_one({"user_id": 3},{'$set':{"epccount%i" %i:0}})
					if keyidlist[i-1] == "-":
						mytempepccountcollection.update_one({"user_id": 3},{'$set':{"epccount%i" %i:1}})

				for doc_tempepccount in findTempEPCCount:
					for i in range(1,101):
						globals()["tempepccount" + str(i)]=doc_tempepccount["epccount%i" %i]

				for i in range(1,101):
					if globals()["tempepccount" + str(i)]>abs(0):
						myTempKeycollection.update_one({"user_id": 3},{'$set':{"Tag%i" %i:1}})
						count1 = count1+1
					else:
						myTempKeycollection.update_one({"user_id": 3},{'$set':{"Tag%i" %i:0}})
				tempepckeylist = get_list.tempepckey_list(3)
				key_name_identifier,status_identifier, id_identifier, indexlist,usr_name_identifier = ([] for i in range(5))
				for i in range(1,101):
					if epckeylist[i-1] != tempepckeylist[i-1]:
						if tempepckeylist[i-1] == 1:
							myKeycollection.update_one({"user_id": 3},{'$set':{"Tag%i" %i:1}})
							df = pd.DataFrame(data = {"user_id": 3, "日付" : str(date_only),"時刻" : str(dday), '状況' : "返却", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							df1=pd.DataFrame()

							print(df)
							# if flag ==0 :
							# print("This is df")
							# df1=df.drop_duplicates()
							x=myrecordcollection.insert_many(df.to_dict('records'))
							# flag=1
							# db.collection.ensureIndex( { record_id:1 }, { unique:true, dropDups:true } )

							# print(df1)
							
						else:
							myKeycollection.update_one({"user_id": 3},{'$set':{"Tag%i" %i:0}})
							mynamecollection.update_one({"user_id": 3},{'$set':{"name%i"  %i:name}})
							mydaycollection.update_one({"user_id": 3},{'$set':{"day%i" %i:d_day}})
							mymonthcollection.update_one({"user_id": 3},{'$set':{"month%i"  %i:d_month}})
							myhourcollection.update_one({"user_id": 3},{'$set':{"hour%i"  %i:d_hour}})
							myminutecollection.update_one({"user_id": 3},{'$set':{"minute%i"  %i:d_min}})
							mydeptcollection.update_one({"user_id": 3},{'$set':{"dept%i"  %i:dept_name}})
							df = pd.DataFrame(data = {"user_id": 3, "日付" : str(date_only),"時刻" : str(dday), '状況' : "貸出", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							print(df)
							# df=df.drop_duplicates()
							# print(df)
							# if flag ==0 :
							x=myrecordcollection.insert_many(df.to_dict('records'))
							# flag=1
						
			
			except:
				logger_1.error("EmptyDataError: No Columns to read from empty CSV file...")

			mystatecollection.update_one({"user_id": 3},{'$set':{"state": "0"}})

		

		#html list
		ukeylist       = get_list.tempkey_list(3)
		unamelist      = get_list.name_list(3)
		ucompnamelist  = get_list.compname_list(3)
		umonthlist     = get_list.month_list(3)
		udaylist       = get_list.day_list(3)
		uhourlist      = get_list.hour_list(3)
		uminutelist    = get_list.minute_list(3)
		ukeycolorlist  = get_list.keycolor_list(3)
		unokeycolorlist  = get_list.nokeycolor_list(3)

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]
		
def box4():
	while True:
		flag=0
		findInfo = myinfocollection.find(filter = { "user_id" : 4})
		Room=[]
		for doc_info in findInfo:
			fullname=doc_info["fullname"]
			name=doc_info["name"]
			dept_name=doc_info["dept_name"]
			dept=doc_info["dept"]
			dday=doc_info["dday"]
			date_only=doc_info["date_only"]
			d_month=doc_info["d_month"]
			d_day=doc_info["d_day"]
			d_hour=doc_info["d_hour"]
			d_min=doc_info["d_min"]
			d_sec=doc_info["d_sec"]
			currsecond=d_sec

		#Assign individual variable to Take Out the Data from each Database Collection
		# print("inside 3 part1")
		findTempEPCCount = mytempepccountcollection.find(filter = { "user_id" : 4})
		findState = mystatecollection.find(filter = { "user_id" : 4})
		findCheck = mycheckcollection.find(filter = { "user_id" : 4})
		findCondition = myconditioncollection.find(filter = { "user_id" : 4})
		findRpiData = myrpidatadbcollection.find()
		findZebraData = myzebraalertcollection.find()
		findRPIError  = myrpicheckalertcollection.find()


		#python list
		epckeylist     = get_list.epckey_list(4)
		epcnamelist    = get_list.epcname_list(4)
		epckeyboxlist  = get_list.epckeybox_list(4)
		keyidlist      = get_list.keyid_list(4)
		rentcomplist   = get_list.rentcomp_list(4)
		rentcompidlist = get_list.rentcompid_list(4)
		roomidlist     = get_list.roomid_list(4)

		#html list
		keynamelist   = get_list.keyname_list(4)
		namelist      = get_list.name_list(4)
		compnamelist  = get_list.compname_list(4)
		monthlist     = get_list.month_list(4)
		daylist       = get_list.day_list(4)
		hourlist      = get_list.hour_list(4)
		minutelist    = get_list.minute_list(4)
		keycolorlist  = get_list.keycolor_list(4)
		nokeycolorlist  = get_list.nokeycolor_list(4)
		firstkeylist  = get_list.key_list(4)
		secondkeylist = get_list.key_list(4)

		#condition variables
		# print("check 4")
		for doc_state in findState:
			state=doc_state["state"]

		for doc_check in findCheck:
			check=doc_check["check"]

		for doc_condition in findCondition:
			condition=doc_condition["condition"]

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]	

		if condition=="0":
			mycheckcollection.update_one({"user_id": 4},{'$set':{"check": "1"}})
			mystatecollection.update_one({"user_id": 4},{'$set':{"state": "1"}})
		
		if condition=="1" and state=="1":
			logger_1.info('Box4 has been opened...')
			if check=="1":
				logger_1.info('Checking the keys and Updating the Page...')
				mycheckcollection.update_one({"user_id": 4},{'$set':{"check": "0"}})
			
			time.sleep(5.5)
				
			
			try:
				logger_1.info('Reading \"test11.csv\"...')
				epcreader_df= pd.read_csv("C:\\Zebra\\test11.csv", engine='python')
				count1 = 0 
				
				for i in range(1,101):
					if keyidlist[i-1] in epcreader_df.values:
						number=epcreader_df[epcreader_df['EPCID'] == keyidlist[i-1]].index[0]
						datacount = int(epcreader_df["Count"][number])
						mytempepccountcollection.update_one({"user_id": 4},{'$set':{"epccount%i" %i:datacount}})
					elif keyidlist[i-1] not in epcreader_df.values:
						if keyidlist[i-1] == "-" or epcnamelist[i-1] == "-":
							mytempepccountcollection.update_one({"user_id": 4},{'$set':{"epccount%i" %i:1}})
						else:
							mytempepccountcollection.update_one({"user_id": 4},{'$set':{"epccount%i" %i:0}})
					if keyidlist[i-1] == "-":
						mytempepccountcollection.update_one({"user_id": 4},{'$set':{"epccount%i" %i:1}})

				for doc_tempepccount in findTempEPCCount:
					for i in range(1,101):
						globals()["tempepccount" + str(i)]=doc_tempepccount["epccount%i" %i]

				for i in range(1,101):
					if globals()["tempepccount" + str(i)]>abs(0):
						myTempKeycollection.update_one({"user_id": 4},{'$set':{"Tag%i" %i:1}})
						count1 = count1+1
					else:
						myTempKeycollection.update_one({"user_id": 4},{'$set':{"Tag%i" %i:0}})
				tempepckeylist = get_list.tempepckey_list(4)
				key_name_identifier,status_identifier, id_4dentifier, indexlist,usr_name_identifier = ([] for i in range(5))
				for i in range(1,101):
					if epckeylist[i-1] != tempepckeylist[i-1]:
						if tempepckeylist[i-1] == 1:
							myKeycollection.update_one({"user_id": 4},{'$set':{"Tag%i" %i:1}})
							df = pd.DataFrame(data = {"user_id": 4, "日付" : str(date_only),"時刻" : str(dday), '状況' : "返却", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							x=myrecordcollection.insert_many(df.to_dict('records'))
							print(df)
							
						else:
							myKeycollection.update_one({"user_id": 4},{'$set':{"Tag%i" %i:0}})
							mynamecollection.update_one({"user_id": 4},{'$set':{"name%i"  %i:name}})
							mydaycollection.update_one({"user_id": 4},{'$set':{"day%i" %i:d_day}})
							mymonthcollection.update_one({"user_id": 4},{'$set':{"month%i"  %i:d_month}})
							myhourcollection.update_one({"user_id": 4},{'$set':{"hour%i"  %i:d_hour}})
							myminutecollection.update_one({"user_id": 4},{'$set':{"minute%i"  %i:d_min}})
							mydeptcollection.update_one({"user_id": 4},{'$set':{"dept%i"  %i:dept_name}})
							df = pd.DataFrame(data = {"user_id": 4, "日付" : str(date_only),"時刻" : str(dday), '状況' : "貸出", 'キー名': epcnamelist[i-1], '部署名': dept, '貸出者': fullname, "タグID" : keyidlist[i-1], "キーボックスNo" : epckeyboxlist[i-1], "レンタル会社" : rentcomplist[i-1], "番号" : rentcompidlist[i-1]}, index=[0])
							print(df)
							x=myrecordcollection.insert_many(df.to_dict('records'))
						
			
			except:
				logger_1.error("EmptyDataError: No Columns to read from empty CSV file...")

			mystatecollection.update_one({"user_id": 4},{'$set':{"state": "0"}})

		

		#html list
		ukeylist       = get_list.tempkey_list(4)
		unamelist      = get_list.name_list(4)
		ucompnamelist  = get_list.compname_list(4)
		umonthlist     = get_list.month_list(4)
		udaylist       = get_list.day_list(4)
		uhourlist      = get_list.hour_list(4)
		uminutelist    = get_list.minute_list(4)
		ukeycolorlist  = get_list.keycolor_list(4)
		unokeycolorlist  = get_list.nokeycolor_list(4)

		#greenred
		for doc_rpidata in findRpiData:
			rpidata=doc_rpidata["rpistatus"]

		for eror_code in findZebraData:
			zebradata=eror_code["Error_code"]
			# logger_1.info(zebradata) 

		for rpi_code in findRPIError:
			rpierror=rpi_code["RPIError_code"]



if __name__ == '__main__':
	pid = os.getpid()
	mykagipiddbcollection.update_one({"user_id": 1},{'$set':{"pid": pid}})
	root_logger= logging.getLogger()
	root_logger.setLevel(logging.DEBUG)
	handler = TimedRotatingFileHandler('C:\\Face\\log1\\MainPage.log', when='D', interval = 1, backupCount=1, encoding='utf-8')
	handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
	root_logger.addHandler(handler)	

	findSYSIPData = mysysipdatadbcollection.find()
	for doc_rpidata in findSYSIPData:
		ipdata=doc_rpidata["sysip_address"] 
	
	logger_1.info("Current system ipaddress")
	logger_1.info(ipdata)
	
	t1 = threading.Thread(target=rpspberryPiRun)
	t1.setDaemon(True)
	t1.start()

	t2 = threading.Thread(target=kanripart1Class)
	t2.setDaemon(True)
	t2.start()

	t3 = threading.Thread(target=kanripart2Class)
	t3.setDaemon(True)
	t3.start()

	t4 = threading.Thread(target=ZebraConnection)
	t4.setDaemon(True)
	t4.start()

	t5 = threading.Thread(target=box1)
	t5.setDaemon(True)
	t5.start()

	t6 = threading.Thread(target=box2)
	t6.setDaemon(True)
	t6.start()

	t7 = threading.Thread(target=box3)
	t7.setDaemon(True)
	t7.start()

	t8 = threading.Thread(target=box4)
	t8.setDaemon(True)
	t8.start()

	server = Server(app.wsgi_app)

	app.run(debug=False, host=ipdata, port="200")		