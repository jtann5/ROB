import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)

x = 0
while True:
    response = ser.readline()
    print(response.decode().strip())  # Decode bytes to string and remove newline characters
    if x > 20:
        break
    else:
        x+=1
        time.sleep(2)

# Close serial connection
ser.close()