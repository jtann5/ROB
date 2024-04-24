import serial

def readSerial():
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.readline()  # example mc 00 000001ab 00000d7f 0000124c 00000d31 2996 97 000f9bda t7:0 1a38
    response = ser.readline()  # example $KT7,0.45,3.43,4.70,3.36,LO=[no solution]
    while response.decode().strip().split(',')[0] != "$KT7":
        response = ser.readline()
    print(response)
    # print(response.decode().strip())  # Decode bytes to string and remove newline characters

while True:
    readSerial()