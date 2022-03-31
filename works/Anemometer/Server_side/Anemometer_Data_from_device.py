import serial
import time
from datetime import datetime
import threading
import struct

import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://192.168.1.36:5556")

ser = serial.Serial(
 port='/dev/ttyUSB0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=2
)

def test_thread():
    
    
    while True:
        if ser.read()==b'\x00':
            pass
        else:
            data_from_input_buffer = ser.read_until(b'\r').strip(b'\x02').rstrip() # because sometimes \r comes as header and tail without \x02
            receive_data_from_ev = data_from_input_buffer.decode("utf-8")
            
            if receive_data_from_ev[2:4] == "08": #here 08 for wind in m/s
           
                if receive_data_from_ev[5] == "0" :   #checking the decimal point at 5 bit
                   en2 = float(receive_data_from_ev[-4:])
                   
                elif receive_data_from_ev[5] =="1" :  #checking the decimal point at 5 bit and then making the value to that decimal point
                   
                   en2 = float(receive_data_from_ev[-4:])
                   en2 = en2/10
                   #print(en2)
                
                elif receive_data_from_ev[5] =="2":
                
                   en2 = float(receive_data_from_ev[-4:])
                   en2 = en2/100
                   
                elif receive_data_from_ev[5] =="3":
                    
                   en2 = float(receive_data_from_ev[-4:])
                   en2 = en2/1000
                   #print(en2)   


                json = {
                "Anemo" : {
                    "Wind_speed in m/s" : en2
                    }
                }
                socket.send_json(json)
                #print(json["Anemo"])
        time.sleep(.01)

if __name__ == '__main__':
    
    anemo_thread = threading.Thread(target=test_thread)
    
    anemo_thread.start()

    
  
  

    
    

