import math
import time
import serial
from rob import rob

# rob.defaults()
# run get position
# rob.setMotor(4, 6000) # turn head one way
# run get position
# rob.setMotor(4, 4000) # turn head opposite way
# run get position
# get the vector for rob
# dot product robs orientation with the Anchor Rob vector for angle
# turn until the dot product is close enough (need to figure that number out)

distance = 3

anchor0 = [0, 3]
anchor1 = [3, 3]
anchor2 = [3, 0]
anchor3 = [0, 0]

anchors = [anchor0, anchor1, anchor2, anchor3]


def readSerial():
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.readline()  # example mc 00 000001ab 00000d7f 0000124c 00000d31 2996 97 000f9bda t7:0 1a38
    response = ser.readline()  # example $KT7,0.45,3.43,4.70,3.36,LO=[no solution]
    while response.decode().strip().split(',')[0] != "$KT7":
        response = ser.readline()
    print(response)
    # print(response.decode().strip())  # Decode bytes to string and remove newline characters
    arr = response.decode().strip().split(',')
    float_array = [float(x) for x in arr[1:5]]
    print("A0: " + str(float_array[0]) + "m")
    print("A1: " + str(float_array[1]) + "m")
    print("A2: " + str(float_array[2]) + "m")
    print("A3: " + str(float_array[3]) + "m")
    print("Quad: " + str(float_array.index(min(float_array))))
    print("")
    ser.close()
    return float_array

def calcPosition(coords):
    closestAnchor = coords.index(min(coords))
    original_val = coords[closestAnchor]
    coords[closestAnchor] = 100
    secondClosestAnchor = coords.index(min(coords))
    coords[closestAnchor] = original_val

    x_coord = ((distance ** 2) - (secondClosestAnchor ** 2) + (closestAnchor ** 2)) / (2 * distance)
    y_coord = math.sqrt((closestAnchor ** 2) - (x_coord ** 2))

    return x_coord, y_coord

def vectorDetector(initalx, initaly, finalx, finaly):
    return finalx - initalx, finaly - initaly

def dotProduct(vector1x, vector1y, vector2x, vector2y):
    return vector1x * vector2x + vector1y * vector2y

def getRobProduct(type):
    rob.defaults()
    print("ROBS COORDINATES")
    rob_coords = readSerial()
    print("ROB P1")
    time.sleep(1000)
    rob.setMotor(4, 6000)
    rob1 = readSerial()
    print("ROB P2")
    time.sleep(1000)
    rob.setMotor(4, 4000)
    rob2 = readSerial()
    time.sleep(1000)
    rob.defaults()

    robposx, robposy = calcPosition(rob_coords)
    type.robposx = robposx
    type.robposy = robposy
    closestAnchor = rob_coords.index(min(rob_coords))
    if not type.said:
        rob.say("Quadrant " + str(closestAnchor))
        type.said = True
    type.closestAnchor = closestAnchor
    initialx = anchors[closestAnchor][0]
    initialy = anchors[closestAnchor][1]
    type.initialx = initialx
    type.initialy = initialy
    anchorVectorX, anchorVectorY = vectorDetector(initialx, initialy, robposx, robposy)
    type.anchorVectorX = anchorVectorX
    type.anchorVectorY = anchorVectorY

    roborienx1, roborieny1 = calcPosition(rob1)
    roborienx2, roborieny2 = calcPosition(rob2)
    type.roborienx1 = roborienx1
    type.roborieny1 = roborieny1
    type.roborienx2 = roborienx2
    type.roborieny2 = roborieny2
    robVectorX, robVectorY = vectorDetector(roborienx1, roborieny1, roborienx2, roborieny2)
    type.robVectorX = robVectorX
    type.robVectorY = robVectorY

    robProduct = dotProduct(anchorVectorX, anchorVectorY, robVectorX, robVectorY)
    type.robProduct = robProduct


class Headings:
    def __init__(self):
        self.robposx = 0
        self.robposy = 0
        self.closestAnchor = 0
        self.initialx = 0
        self.initialy = 0
        self.anchorVectorX = 0
        self.anchorVectorY = 0
        self.roborienx1 = 0
        self.roborieny1 = 0
        self.roborienx2 = 0
        self.roborieny2 = 0
        self.robVectorX = 0
        self.robVectorY = 0
        self.robProduct = 0
        self.said = False

if __name__ == "__main__":
    heading = Headings()
    getRobProduct(heading)

    
    rob.defaults()
    rob.say('Exited')

'''
while True:
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.readline() # example mc 00 000001ab 00000d7f 0000124c 00000d31 2996 97 000f9bda t7:0 1a38
    response = ser.readline()  # example $KT7,0.45,3.43,4.70,3.36,LO=[no solution]
    while response.decode().strip().split(',')[0] != "$KT7":
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
'''
