import serial
import time

x = 0
while True:
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.readline() # example mc 00 000001ab 00000d7f 0000124c 00000d31 2996 97 000f9bda t7:0 1a38
    response = ser.readline()  # example $KT7,0.45,3.43,4.70,3.36,LO=[no solution]
    #print(response.decode().strip())  # Decode bytes to string and remove newline characters
    arr = response.decode().strip().split(',')
    print("A0: " + arr[1] + "m")
    print("A1: " + arr[2] + "m")
    print("A2: " + arr[3] + "m")
    print("A3: " + arr[4] + "m")
    ser.close()
    if x > 100:
        break
    else:
        x+=1
        time.sleep(0.5)
