import pygatt
from binascii import hexlify
#import uuid
import logging
import time
from time import sleep
#import re
import numpy as np
import pandas as pd


logging.basicConfig(filename ='testfile1.txt',filemode='w',level=logging.DEBUG)
testtext = logging.getLogger('pygatt').setLevel(logging.DEBUG)
#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.INFO)

 
# Initialize the adaptor at the very beginning
adapter = pygatt.GATTToolBackend()

# Declaring the DataFrame for the first time
d = pd.DataFrame()


#The following function is for 2's compliment of the  summation
def tohex(val,nbits):
    return hex((val + (1 << nbits)) % (1 << nbits)).upper()

#The following function will work to minimize painstalking command conversion
def transform_command(manual_input):
    #Input command in a string form


    ## First fixed header
    fixed_header  = bytearray([0x02,0x30,0x30,0x30,0x30,])

    ## Input raw command to be joined after 
    raw_input = manual_input
    # convert the raw input into byte array
    input_into_byte = bytearray(raw_input,'ascii')

    ## Join the First two parts
    fixed_header.extend(input_into_byte)

    ## Join end of command (ETX)
    fixed_header.append(0x03)

    ## Hexadecimal summation of all the previous bytes
    total_sum = 0 - int(hex(sum(fixed_header)),16) #*# 16 is to ensure it is a hex
    
    ## Take the last two bits as ascii characters
    fixed_header.extend(bytearray(tohex(total_sum,64)[-2:],'ascii'))

    ## Join end of transmission (EOT) and making final command
    fixed_header.append(0x04)
    final_command = fixed_header

    #test
    print(final_command)
    return final_command


# The following function will work only if the main command contains LI
# Objective is to have a look on different combination of tables found in the datasheet
def transform_command_LI(manual_input):
    #Input command in a string form


    ## First fixed header
    fixed_header  = bytearray([0x02,0x30,0x30,0x30,0x30,])

    ## Input raw command to be joined after 
    raw_input = manual_input
    # convert the raw input into byte array
    input_into_byte = bytearray(raw_input,'ascii')

    ## Join the First two parts
    fixed_header.extend(input_into_byte)

    ## Join end of command (ETX)
    fixed_header.append(0x03)

    ## Hexadecimal summation of all the previous bytes
    total_sum = 0 - int(hex(sum(fixed_header)),16) #*# 16 is to ensure it is a hex
    
    ## Take the last two bits as ascii characters
    fixed_header.extend(bytearray(tohex(total_sum,64)[-2:],'ascii'))

    ## Join end of transmission (EOT) and making final command
    fixed_header.append(0x04)
    final_command = fixed_header

    #test
    print(final_command)
    return final_command

#The following function trimms the output data as a string format and send to table formatting function
def printdata(file):
    
    #file = open(filename,"r")
    #line = file.readline()
    
    data = ""
    for x in file:
    #while line:
        # initializing string  
        test_string = x
        if x.startswith('INFO:pygatt.device:Received notification on handle=0xd, value=0xb'):
        #if line.startswith('INFO:pygatt.device:Received notification on handle=0xd, value=0xb'):
        # initializing split word 
            spl_word = "INFO:pygatt.device:Received notification on handle=0xd, value=0xb'"
                      
            # using partition() 
            # Get String after substring occurrence 
            res = test_string.partition(spl_word)[2][:-2]
            #res = line.partition(spl_word)[2][:-2]
            res2 = bytes.fromhex(res)
            res3 = res2.decode("ASCII")
            data = data + res3
            sleep(0.50)
            # print result 
            # print(res3)
    table_data(data)
    
    
#The following function formats the data as a table looking format
def table_data(data):
    
    #THIS SLEEP IS FOR PROCESSING TIME. OTHERWISE IT CANNOT TRIM THE UNNECESSARY DATAS
    #sleep(1)
    
    #Start trimming
    trimmed_data = data.split(",")[2:-1]  #Because first two and the last data represents Address channel, command, and etx&SUM respectively
    
    
    #The global keyword is needed when accessing the global variable
    global d
    
    
    # just random experiment
    # As it turned out its actually beneficial to transform data into numpy array
    a = np.array(trimmed_data)
    
    # This removes the problem of empty DataFrame
    if d.empty:
        #d = pd.DataFrame(a)
        
        #Ths part is only for data of current value. Convert it to different function later
        d = pd.DataFrame({'H2'  :  [a[5]],
                          'O2'  :  [a[6]],
                          'H2S' :  [a[7]],
                          'CO'  :  [a[8]],
                          'CO2' :  [a[9]]
                          })
    
    else:
        #new = pd.DataFrame(a)
        
        new = pd.DataFrame({'H2'  :  [a[5]],
                            'O2'  :  [a[6]],
                            'H2S' :  [a[7]],
                            'CO'  :  [a[8]],
                            'CO2' :  [a[9]]
                          })
        join_data(new)
    
#     for k in range(len(trimmed_data)):
#         print("Data " + str(k+1) +": " + trimmed_data[k])



# The following function is a try to join the datas in a DataFrame
def join_data(dataset):
    global d
    
    #f = pd.concat([d,dataset] , axis=1)
    
    f = d.append(dataset, ignore_index = True)
    
    d = f
    
    print(d)


try:
    adapter.start()
    #print(adapter.filtered_scan)
    #sleep(1)
    device = adapter.connect('E1:3E:40:2A:9D:C5', address_type=pygatt.BLEAddressType.random)
    #sleep(1)
    
    # Initialize dataframe
    
    
    characteristicsTx_1 = "5699d646-0c53-11e7-93ae-92361f002671"
    characteristicsRx_1 = "5699d772-0c53-11e7-93ae-92361f002671"
    characteristicsTx_2 = "5699d647-0c53-11e7-93ae-92361f002671"
    characteristicsRx_2 = "5699d773-0c53-11e7-93ae-92361f002671"
    
    #first switch on the notification handle of tx uuid
    device.char_write_handle(0x000e, bytearray([0x01,0x00]))
    
    # prompt and take input
#     print("Provide a valid input")
#     user_input = input().upper()
    # But for the time being
    user_input = "DH,R,"
    
    
    # Send input to process
    final_command = transform_command(user_input)
    
    # Open file once   
    file = open("testfile1.txt","r")

    if str(user_input).find("li".upper()) != -1:
        trim_inpt = user_input.split(",")
        for i in range(5):
            for k in range(29):
                trim_inpt[2] = format(i,'02X')
                trim_inpt[3] = format(k,'02X')
                user_input = ','.join(map(str,trim_inpt))
                final_command = transform_command(user_input)
                device.char_write(characteristicsRx_1,final_command,wait_for_response=True)
                
                sleep(0.250)
                #parse data from txt file
                #fl = "testfile1.txt"
                printdata(file)
                
                
                
    elif str(user_input).find("dh".upper()) != -1:
        #for jo in range(20):
        while True:            
            device.char_write(characteristicsRx_1,final_command,wait_for_response=True)
            
            sleep(0.250)
            
            printdata(file)
            
            
    
                
    else:
        device.char_write(characteristicsRx_1,final_command,wait_for_response=True)
        
        sleep(0.250)
        
        printdata(file)
    

            
finally:
    adapter.stop()

