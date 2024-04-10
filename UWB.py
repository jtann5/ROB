import serial

while True:
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.readline() # example mc 00 000001ab 00000d7f 0000124c 00000d31 2996 97 000f9bda t7:0 1a38
    response = ser.readline()  # example $KT7,0.45,3.43,4.70,3.36,LO=[no solution]
    while response.decode.strip.split(',')[0] != "$KT7":
        response = ser.readline()
    print(response)
    #print(response.decode().strip())  # Decode bytes to string and remove newline characters
    arr = response.decode().strip().split(',')
    float_array = [float(x) for x in arr[1:5]] 
    print("A0: " + str(float_array[0]) + "m")
    print("A1: " + str(float_array[1]) + "m")
    print("A2: " + str(float_array[2]) + "m")
    print("A3: " + str(float_array[3]) + "m")
    print("Quad: " + str(float_array.index(min(float_array))))
    print("")
    ser.close()
        
    if input().lower() == "exit":
        break

