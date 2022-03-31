#!/usr/bin/python
from datetime import datetime
import RPi.GPIO as GPIO
import socket, time, sys, logging,os
from logging.handlers import TimedRotatingFileHandler

logger= logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler('/home/pi/log folder/ServerLog.log', when='D', interval=2, backupCount=1, encoding='utf-8')
#os.chmod("/home/pi/log folder/ServerLog.log",0o777)
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(handler)

#pin number declaration BOX 3 and 4 
pushbutton1 = 6
key1 = 17 
red1 = 27
green1 = 18
buzz1 = 23


pushbutton2 = 13
key2 = 24
red2 = 25
green2 = 8
buzz2 = 7

pushbutton3 = 19
key3 = 12
red3 = 16
green3 = 20
buzz3 = 21

pushbutton4 = 26
key4 =22 
red4 = 10
green4 = 9
buzz4 = 11

# pushbutton1 = 19
# key1 = 12
# red1 = 27
# green1 = 18
# buzz1 = 23
# 
# 
# pushbutton2 = 26
# key2 = 22
# red2 = 25
# green2 = 8
# buzz2 = 7
# 
# pushbutton3 = 6
# key3 = 17
# red3 = 16
# green3 = 20
# buzz3 = 21
# 
# pushbutton4 = 13
# key4 =24
# red4 = 10
# green4 = 9
# buzz4 = 11


#variable declaration
sendData = "Connected"
buttonstate = state = log = 1
datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
logstatus = ""

box_1 = box_2 = box_3 = box_4 = 0
wait = 0 #variable used for closing doors and green LEDs shut down immediately

#mode set up
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pin set up
#GPIO.setup(pushbutton1, GPIO.IN)
GPIO.setup(pushbutton1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# ~ GPIO.setup(pushbutton2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# ~ GPIO.setup(pushbutton1, GPIO.IN)
# ~ GPIO.setup(pushbutton1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pushbutton2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pushbutton3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(pushbutton4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(key1, GPIO.OUT)
GPIO.setup(red1, GPIO.OUT)
GPIO.setup(green1, GPIO.OUT)
GPIO.setup(buzz1, GPIO.OUT)

GPIO.setup(key2, GPIO.OUT)
GPIO.setup(red2, GPIO.OUT)
GPIO.setup(green2, GPIO.OUT)
GPIO.setup(buzz2, GPIO.OUT)

GPIO.setup(key3, GPIO.OUT)
GPIO.setup(red3, GPIO.OUT)
GPIO.setup(green3, GPIO.OUT)
GPIO.setup(buzz3, GPIO.OUT)

GPIO.setup(key4, GPIO.OUT)
GPIO.setup(red4, GPIO.OUT)
GPIO.setup(green4, GPIO.OUT)
GPIO.setup(buzz4, GPIO.OUT)

# ~ port and hostname set up
port1 = 12345
port2 = 5000

# ~ port and hostname set up
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '192.168.1.112'
s1.bind((host, port1))
s1.listen(1)
c, addr = s1.accept()
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.bind((host, port2))
s2.listen(1)
server_port2, addr2 = s2.accept()

while True:
	try:
		c.send(sendData.encode())
		buttonstate1 = GPIO.input(pushbutton1)
		buttonstate2 = GPIO.input(pushbutton2)
		buttonstate3 = GPIO.input(pushbutton3)
		buttonstate4 = GPIO.input(pushbutton4)
		receivedData = c.recv(1024).decode()
		alertseconds = server_port2.recv(1024).decode()
		# print("box1 : " + str(buttonstate1))
		# print("box2 : " + str(buttonstate2))
		# print("box3 : " + str(buttonstate3))
		# print("received: " + str(receivedData))
		
		#function to turn ON the desired keys and lamps
		def gpioOutputON(*args):
			for pin in args:
				GPIO.output(pin, GPIO.HIGH)

		#function to turn OFF the desired keys and lamps
		def gpioOutputOFF(*args):
			for pin in args:
				GPIO.output(pin, GPIO.LOW)

		#when all boxes are closed
		if buttonstate1 == 0 and buttonstate2 == 0 and buttonstate3 == 0 and buttonstate4 == 0:
			buttonstate = "4BoxClosed" #variable that confirms all 3 boxes are closed
			state = 1 #variable to make sure that start time is counted for only once

		#when the door is closed, turn off the keys and lamps immediately
		if receivedData == "OFF":
			wait = 0
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
		
		#when face is recognized, turn on the keys and lamps immediately
		if receivedData == "ON" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0
			
			sendData = "StartTimeCount" #tell computer to count 7 seconds after face recognition
			gpioOutputON(key1, green1, key2, green2, key3, green3, key4, green4)
			
		#when the 7 seconds count is reached, turn off the keys and lamps immediately
		if receivedData == "AutoClose" and buttonstate == "4BoxClosed":
			log = 1
			sendData = "SelfClosed" #tell computer that none of the boxes is being opened
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			
		#when box1 person face is recognized, turn on the keys and lamps of box1 immediately
		if receivedData == "1" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1)
			gpioOutputOFF(key2, green2, key3, green3, key4, green4)
			
		#######################################################################
		
		if receivedData == "12" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1,key2, green2)
			#gpioOutputOFF(key3, green3, key4, green4)
			#gpioOutputON(key2, green2)
			#gpioOutputOFF(key1, green1, key3, green3, key4, green4)
		
				
		if receivedData == "13" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1,key3, green3)
		if receivedData == "14" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1,key4, green4)
		if receivedData == "23" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key2, green2,key3, green3)
		if receivedData == "24" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key2, green2,key4, green4)
		if receivedData == "34" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key3, green3,key4, green4)
		if receivedData == "123" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1,key2, green2,key3, green3)
		
		if receivedData == "124" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1,key2, green2,key4, green4)
			
		if receivedData == "134" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key1, green1,key3, green3,key4, green4)
				
			
				
		if receivedData == "234" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key2, green2,key3, green3,key4, green4)						
		
		######################################################################################	
			
			
		if receivedData == "2" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key2, green2)
			gpioOutputOFF(key1, green1, key3, green3, key4, green4)
			
		if receivedData == "3" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key3, green3)
			logger.info("Receive3")
			gpioOutputOFF(key1, green1, key2, green2, key4, green4)

		if receivedData == "4" and buttonstate == "4BoxClosed" and wait == 0:
			if log:
				datetimeVar = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
				log = 0

			sendData = "StartTimeCount"
			gpioOutputON(key4, green4)
			gpioOutputOFF(key1, green1, key2, green2, key3, green3)	

		#when box1 is being opened, send "box1" to computer
		if box_1 and buttonstate == "4BoxClosed":
			log = 1 #save log for only once
			wait = 1 #since wait became 1, doors and green LEDs are closed although received data is "ON"
			sendData = "box1"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_1 = 0 #make sure that this condition worked for only once
			
		if box_2 and buttonstate == "4BoxClosed":
			log = 1 #save log for only once
			wait = 1 
			sendData = "box2"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_2 = 0 
			
		if box_3 and buttonstate == "4BoxClosed":
			log = 1 #save log for only once
			wait = 1 
			sendData = "box3"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_3 = 0

		if box_4 and buttonstate == "4BoxClosed":
			log = 1 #save log for only once
			wait = 1 
			sendData = "box4"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_4 = 0	

		#algorithm for saving log file
		if datetimeVar == str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]):
			logger.info("box1 : " + str(buttonstate1))
			logger.info("box2 : " + str(buttonstate2))
			logger.info("box3 : " + str(buttonstate3))
			logger.info("box4 : " + str(buttonstate4))
			logger.info("received: " + str(receivedData))

		#when box1 is being opened, send turn off the green lamps
		if buttonstate1 == 1 and buttonstate2 == 0 and buttonstate3 == 0 and buttonstate4 == 0:
			box_1 = 1 #variable used to send "box1" to computer
			buttonstate = "BoxOpen" #one of the boxes is opened, so the value is no more "3BoxClosed"
			# print("box1 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key2, key3, key4)

			#time count has started when the box is opened
			start_time = time.time()
			if state:
				state = 0 #make sure that this condition worked for only once
				end_time = start_time + int(alertseconds) #seconds to alert are added to start time
			
			
			# def shut_down(channel): # Long Press to shutdown
				# if channel == pushbutton1:
					# sw = 0
					# for _ in range(15):
						# time.sleep(0.2) # 0.2 seconds x 15 times = 3 seconds
						# sw = GPIO.input(channel)
						# print(sw)
						# if sw == 0: # If there is even one LOW out of 15 times, it will not shutdown.
							# break
					# if sw == 1:
						# pass
						# #GPIO.output(PIN_BUTTON_LED, GPIO.LOW) # Button LED off
					# #os.system('sudo shutdown -h now') # shutdown

			
			# #print(buttonstate1)
			# GPIO.add_event_detect(pushbutton1, GPIO.RISING, callback=shut_down, bouncetime=200)
		
			buttonstate1 = GPIO.input(pushbutton1)
			if buttonstate1 == 0:
				for _ in range(15):
					time.sleep(0.2)
					
				
			
			print(buttonstate1)
			
			
			#logger.info("box1 : " + str(buttonstate1))
			#print(buttonstate1)
			#if the alert time is reached, turn on the red lamp of box1
			if start_time > end_time and buttonstate1:
				buttonstate1 = GPIO.input(pushbutton1)
				if buttonstate1:
					sendData = "Alert_mp3_box1" #tell computer to play alert mp3 file
					GPIO.output(red1, GPIO.HIGH)
		
		if buttonstate1 == 0 and buttonstate2 == 1 and buttonstate3 == 0 and buttonstate4 == 0:
			box_2 = 1 
			buttonstate = "BoxOpen" 
			# print("box2 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1, key3, key4)

			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate2 = GPIO.input(pushbutton2)
			if buttonstate2 == 0:
				for _ in range(15):
					time.sleep(0.2)
			
			if start_time > end_time and buttonstate2:
				buttonstate2 = GPIO.input(pushbutton2)
				if buttonstate2:
					sendData = "Alert_mp3_box2" 
					GPIO.output(red2, GPIO.HIGH)
		
		if buttonstate1 == 0 and buttonstate2 == 0 and buttonstate3 == 1 and buttonstate4 == 0:
			box_3 = 1 
			buttonstate = "BoxOpen" 
			# print("box3 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1, key2, key4)


			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate3 = GPIO.input(pushbutton3)
			if buttonstate3 == 0:
				for _ in range(15):
					time.sleep(0.2)
			# logger.info("but3")
			
			if start_time > end_time and buttonstate3:
				buttonstate3 = GPIO.input(pushbutton3)
				if buttonstate3:
					sendData = "Alert_mp3_box3" 
					GPIO.output(red3, GPIO.HIGH)

		if buttonstate1 == 0 and buttonstate2 == 0 and buttonstate3 == 0 and buttonstate4 == 1:
			box_4 = 1 
			buttonstate = "BoxOpen" 
			# print("box3 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1, key2, key3)

			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate4 = GPIO.input(pushbutton4)
			if buttonstate4 == 0:
				for _ in range(15):
					time.sleep(0.2)
			# logger.info("but4")
			
			if start_time > end_time and buttonstate4:
				buttonstate4 = GPIO.input(pushbutton4)
				if buttonstate4:
					sendData = "Alert_mp3_box4" 
					GPIO.output(red4, GPIO.HIGH)			
					
		if buttonstate1 == 1 and buttonstate2 == 1 and buttonstate3 == 1 and buttonstate4 == 1:
			buttonstate = "BoxOpen" 
			# print("All boxes are being opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1, key2, key4)

			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate1 = GPIO.input(pushbutton1)
			if buttonstate1 == 0:
				for _ in range(15):
					time.sleep(0.2)
			buttonstate2 = GPIO.input(pushbutton2)
			if buttonstate2 == 0:
				for _ in range(15):
					time.sleep(0.2)
			buttonstate3 = GPIO.input(pushbutton3)
			if buttonstate3 == 0:
				for _ in range(15):
					time.sleep(0.2)
			buttonstate4 = GPIO.input(pushbutton4)
			if buttonstate4 == 0:
				for _ in range(15):
					time.sleep(0.2)
			
			if start_time > end_time:
				buttonstate1 = GPIO.input(pushbutton1)
				buttonstate2 = GPIO.input(pushbutton2)
				buttonstate3 = GPIO.input(pushbutton3)
				buttonstate4 = GPIO.input(pushbutton4)

				if buttonstate1:
					sendData = "Alert_mp3_box1"
					GPIO.output(red1, GPIO.HIGH)
				if buttonstate2:
					sendData = "Alert_mp3_box2"
					GPIO.output(red2, GPIO.HIGH)
				if buttonstate3:
					sendData = "Alert_mp3_box3"
					GPIO.output(red3, GPIO.HIGH)

				if buttonstate4:
					sendData = "Alert_mp3_box3"
					GPIO.output(red4, GPIO.HIGH)	
					
		#when the door of box1 is reclosed after red lamp ON, turn OFF the red lamp
		if buttonstate1 == 0:
			GPIO.output(red1, GPIO.LOW)
				
		if buttonstate2 == 0:
			GPIO.output(red2, GPIO.LOW)
			
		if buttonstate3 == 0:
			GPIO.output(red3, GPIO.LOW)

		if buttonstate4 == 0:
			GPIO.output(red4, GPIO.LOW)	
	
	#when ctrl + c is pressed, close the sockets and stop the program
	except KeyboardInterrupt:
		logger.info("Manually closed by user...")
		c.close()
		server_port2.close()
		sys.exit()
	
	#when error has been raised, try to connect the socket connects again
	except Exception as e:
		# print(e)
		logger.error(e)
		
		sendData = "Connected"
		
		#trying to connect the sockets and ports again
		s1.listen(1) 
		s2.listen(1)
		c, addr = s1.accept()
		server_port2, addr2 = s2.accept()
		
		#starting the send/receive transmission again
		c.send(sendData.encode())
		receivedData=c.recv(1024).decode()
		alertseconds=server_port2.recv(1024).decode()
		# print("box1 : " + str(buttonstate1))
		# print("box2 : " + str(buttonstate2))
		# print("box3 : " + str(buttonstate3))
		# print("received: " + str(receivedData))

		def gpioOutputON(*args):
			for pin in args:
				GPIO.output(pin, GPIO.HIGH)

		def gpioOutputOFF(*args):
			for pin in args:
				GPIO.output(pin, GPIO.LOW)

		if buttonstate1 == 0 and buttonstate2 == 0 and buttonstate3 == 0 and buttonstate4 == 0:
			buttonstate = "4BoxClosed" 
			state = 1 

		if receivedData == "OFF":
			wait = 0
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
		
		if receivedData == "ON" and buttonstate == "4BoxClosed" and wait == 0:
			sendData = "StartTimeCount" 
			gpioOutputON(key1, green1, key2, green2, key3, green3, key4, green4)
			
		if receivedData == "AutoClose" and buttonstate == "4BoxClosed":
			sendData = "SelfClosed" 
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			
		if receivedData == "1" and buttonstate == "4BoxClosed" and wait == 0:
			sendData = "StartTimeCount"
			gpioOutputON(key1, green1)
			gpioOutputOFF(key2, green2, key3, green3, key4, green4)
			
		if receivedData == "2" and buttonstate == "4BoxClosed" and wait == 0:
			sendData = "StartTimeCount"
			gpioOutputON(key2, green2)
			gpioOutputOFF(key1, green1, key3, green3, key4, green4)
			
		if receivedData == "3" and buttonstate == "4BoxClosed" and wait == 0:
			sendData = "StartTimeCount"
			gpioOutputON(key3, green3)
			#logger.info("Receive again 3")
			gpioOutputOFF(key1, green1, key2, green2, key4, green4)

		if receivedData == "4" and buttonstate == "4BoxClosed" and wait == 0:
			sendData = "StartTimeCount"
			gpioOutputON(key4, green4)
			gpioOutputOFF(key1, green1, key2, green2, key3, green3)
	

		if box_1 and buttonstate == "4BoxClosed":
			wait = 1 
			sendData = "box1"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_1 = 0 
			
		if box_2 and buttonstate == "4BoxClosed":
			wait = 1 
			sendData = "box2"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_2 = 0 
			
		if box_3 and buttonstate == "4BoxClosed":
			wait = 1 
			sendData = "box3"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_3 = 0

		if box_4 and buttonstate == "4BoxClosed":
			wait = 1 
			sendData = "box4"
			gpioOutputOFF(key1, green1, key2, green2, key3, green3, key4, green4)
			box_4 = 0	
			
		if buttonstate1 == 1 and buttonstate2 == 0 and buttonstate3 == 0 and buttonstate4 == 0:
			box_1 = 1 
			buttonstate = "BoxOpen" 
			# print("box1 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key2, key3, key4)
			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate1 = GPIO.input(pushbutton1)
			if start_time > end_time and buttonstate1:
				buttonstate1 = GPIO.input(pushbutton1)
				if buttonstate1:
					sendData = "Alert_mp3_box1" 
					GPIO.output(red1, GPIO.HIGH)
		
		if buttonstate1 == 0 and buttonstate2 == 1 and buttonstate3 == 0 and buttonstate4 == 0:
			box_2 = 1 
			buttonstate = "BoxOpen" 
			# print("box2 opened")
			gpioOutputOFF(green1, green2, green3, green4)	
			gpioOutputOFF(key1, key3, key4)		
			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate2 = GPIO.input(pushbutton2)
			
			if start_time > end_time and buttonstate2:
				buttonstate2 = GPIO.input(pushbutton2)
				if buttonstate2:
					sendData = "Alert_mp3_box2" 
					GPIO.output(red2, GPIO.HIGH)
		
		if buttonstate1 == 0 and buttonstate2 == 0 and buttonstate3 == 1 and buttonstate4 == 0:
			box_3 = 1 
			buttonstate = "BoxOpen" 
			# print("box3 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1, key2, key4)
			
			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate3 = GPIO.input(pushbutton3)
			
			if start_time > end_time and buttonstate3:
				buttonstate3 = GPIO.input(pushbutton3)
				if buttonstate3:
					sendData = "Alert_mp3_box3" 
					GPIO.output(red3, GPIO.HIGH)

		if buttonstate1 == 0 and buttonstate2 == 0 and buttonstate3 == 0 and buttonstate4 == 1:
			box_4 = 1 
			buttonstate = "BoxOpen" 
			# print("box3 opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1, key2, key3)
			
			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate4 = GPIO.input(pushbutton4)
			
			if start_time > end_time and buttonstate4:
				buttonstate4 = GPIO.input(pushbutton4)
				if buttonstate4:
					sendData = "Alert_mp3_box3" 
					GPIO.output(red4, GPIO.HIGH)			
					
		if buttonstate1 == 1 and buttonstate2 == 1 and buttonstate3 == 1 and buttonstate4 == 1:
			buttonstate = "BoxOpen" 
			# print("All boxes are being opened")
			gpioOutputOFF(green1, green2, green3, green4)
			gpioOutputOFF(key1,key2, key3, key4)
			start_time = time.time()
			if state:
				state = 0 
				end_time = start_time + int(alertseconds) 
				
			buttonstate1 = GPIO.input(pushbutton1)
			buttonstate2 = GPIO.input(pushbutton2)
			buttonstate3 = GPIO.input(pushbutton3)
			buttonstate4 = GPIO.input(pushbutton4)
			
			if start_time > end_time:
				buttonstate1 = GPIO.input(pushbutton1)
				buttonstate2 = GPIO.input(pushbutton2)
				buttonstate3 = GPIO.input(pushbutton3)
				buttonstate4 = GPIO.input(pushbutton4)
				if buttonstate1:
					sendData = "Alert_mp3_box1"
					GPIO.output(red1, GPIO.HIGH)
				if buttonstate2:
					sendData = "Alert_mp3_box2"
					GPIO.output(red2, GPIO.HIGH)
				if buttonstate3:
					sendData = "Alert_mp3_box3"
					GPIO.output(red3, GPIO.HIGH)
				if buttonstate4:
					sendData = "Alert_mp3_box3"
					GPIO.output(red4, GPIO.HIGH)	
					
		#when the door of box1 is reclosed after red lamp ON, turn OFF the red lamp
		if buttonstate1 == 0:
			GPIO.output(red1, GPIO.LOW)
				
		if buttonstate2 == 0:
			GPIO.output(red2, GPIO.LOW)
			
		if buttonstate3 == 0:
			GPIO.output(red3, GPIO.LOW)

		if buttonstate4 == 0:
			GPIO.output(red4, GPIO.LOW)	
