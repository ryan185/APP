

import serial
import time
from datetime import datetime
import threading
import struct

import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://192.168.1.36:5555")

def serial_receive_thred():
    
    receive_data_from_ev = ""
    
    while True:
       
        if ser0.in_waiting:    

            rx_buffer_data = ser0.read()
            receive_char = rx_buffer_data.decode()
            receive_data_from_ev = receive_data_from_ev + receive_char
            

            if receive_char == '\r':      # if end of data then convert it array to make arithmatically operationable
                
                converted = []
                for x in receive_data_from_ev.split("OK,DR1,123,"):
                    try:
                       converted.append(int(x, 16))
                       
                       z=(converted[0]*0.298)/200000
                       y=((z-4)/16)*1.5
                       time_measured = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       json = {
                            
                            "Data" : {
                                "Timestamp" : time_measured,
                                "Current value" : y
                            }
                        }
                       socket.send_json(json)
                       #print(json)
                    except Exception as e:
                        pass
                receive_data_from_ev = ""
        time.sleep(.05)


    ser0.close()

def serial_transmit_thred():

    while True:
        
        c_str = "DR1,123" + '\r'
        ser0.write(c_str.encode())


if __name__ == '__main__':
    
    ser0 = None
    while ser0 is None:
        try:
            
            ser0 = serial.Serial('/dev/ttyACM0', 9600)
            
        except:
            print("ser is not connected")
            time.sleep(2)
            pass
    
    

    threding_1 = threading.Thread(target=serial_receive_thred)
    threding_2 = threading.Thread(target=serial_transmit_thred)

    threding_1.start()
    threding_2.start()
    
    time.sleep(1)
    
