import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)

response = ser.readline()
print(response.decode().strip())  # Decode bytes to string and remove newline characters

# Close serial connection
ser.close()