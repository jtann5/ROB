import math
import numpy as np
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
    #print("A0: " + str(float_array[0]) + "m")
    #print("A1: " + str(float_array[1]) + "m")
    #print("A2: " + str(float_array[2]) + "m")
    #print("A3: " + str(float_array[3]) + "m")
    #print("Quad: " + str(float_array.index(min(float_array))))
    #print("")
    ser.close()
    return float_array

def calcPosition(anchors, distances):
    # Convert input lists to NumPy arrays for easier computation
    anchors = np.array(anchors)
    distances = np.array(distances)

    # Number of dimensions (2 for 2D space, 3 for 3D space)
    num_dimensions = anchors.shape[1]

    # Ensure at least as many anchors as dimensions
    if len(anchors) < num_dimensions:
        raise ValueError("Number of anchors must be at least as many as dimensions")

    # Number of anchors
    num_anchors = len(anchors)

    # Calculate distances squared
    distances_squared = distances ** 2

    # Initialize A matrix and b vector
    A = np.zeros((num_anchors - 1, num_dimensions))
    b = np.zeros((num_anchors - 1,))

    # Iterate over pairs of anchors
    for i in range(num_anchors - 1):
        A[i] = 2 * (anchors[i] - anchors[-1])
        b[i] = np.linalg.norm(anchors[i]) ** 2 - np.linalg.norm(anchors[-1]) ** 2 - distances_squared[i] + \
               distances_squared[-1]

    # Calculate least squares solution
    position = np.linalg.lstsq(A, b, rcond=None)[0]

    # Add the position of the reference anchor
    position += anchors[-1]

    return position

def vectorDetector(initalx, initaly, finalx, finaly):
    return finalx - initalx, finaly - initaly

def dotProduct(vector1x, vector1y, vector2x, vector2y):
    return vector1x * vector2x + vector1y * vector2y

def getRobProduct(type):
    rob.defaults()
    time.sleep(1)
    #print("ROBS COORDINATES")
    rob_coords = readSerial()
    time.sleep(1)
    #print("ROB P1")
    rob.setMotor(4, 8000)
    time.sleep(1)
    rob1 = readSerial()
    #print("ROB P2")
    time.sleep(1)
    rob.setMotor(4, 4000)
    time.sleep(1)
    rob2 = readSerial()
    time.sleep(1)
    rob.defaults()
    global anchors
    position = calcPosition(anchors, rob_coords)
    print(position)
    type.robposx = position[0]
    type.robposy = position[1]
    closestAnchor = rob_coords.index(min(rob_coords))
    if not type.said:
        rob.say("Quadrant " + str(closestAnchor))
        type.said = True
    type.closestAnchor = closestAnchor
    initialx = anchors[closestAnchor][0]
    initialy = anchors[closestAnchor][1]
    type.initialx = initialx
    type.initialy = initialy
    if not type.gotAnchorVector:
        anchorVectorX, anchorVectorY = vectorDetector(initialx, initialy, type.robposx, type.robposy)
        type.anchorVectorX = anchorVectorX
        type.anchorVectorY = anchorVectorY
        type.gotAnchorVector = True

    roborienx1, roborieny1 = calcPosition(anchors, rob1)
    roborienx2, roborieny2 = calcPosition(anchors, rob2)
    type.roborienx1 = roborienx1
    type.roborieny1 = roborieny1
    type.roborienx2 = roborienx2
    type.roborieny2 = roborieny2
    robVectorX, robVectorY = vectorDetector(roborienx1, roborieny1, roborienx2, roborieny2)
    type.robVectorX = robVectorX
    type.robVectorY = robVectorY

    robProduct = dotProduct(heading.anchorVectorX, heading.anchorVectorY, robVectorX, robVectorY)
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
        self.gotAnchorVector = False

    def printValues(self):
        print("X: {:.4f}".format(self.robposx))
        print("Y: {:.4f}".format(self.robposy))
        print("Anchor Vector <{:.4f}, {:.4f}>".format(self.anchorVectorX, self.anchorVectorY))
        print("Rob Vector <{:.4f}, {:.4f}>".format(self.robVectorX, self.robVectorY))
        print("ROB Product {:.4f}".format(self.robProduct))


if __name__ == "__main__":
    heading = Headings()
    getRobProduct(heading)

    while ((not heading.robposx < 0 and not heading.robposx > 3) or (not heading.robposy < 0 and not heading.robposy > 3)):
        heading.printValues()
        if heading.robposx < 0 or heading.robposx > 3:
            rob.setMotor(0, 5000)
            rob.setMotor(1, 7000)
            time.sleep(1)
            rob.setMotor(0, 6000)
            rob.setMotor(1, 6000)
            break
        if heading.robposy < 0 or heading.robposy > 3:
            rob.setMotor(0, 5000)
            rob.setMotor(1, 7000)
            time.sleep(1)
            rob.setMotor(0, 6000)
            rob.setMotor(1, 6000)
            break
        #time.sleep(5)
        if heading.robProduct < 0:
            rob.setMotor(0, 5000)
            rob.setMotor(1, 7000)
            time.sleep(0.75)
            rob.setMotor(0, 6000)
            rob.setMotor(1, 6000)
            time.sleep(1)
            getRobProduct(heading)
        else:
            rob.setMotor(0, 5000)
            rob.setMotor(1, 5000)
            time.sleep(0.75)
            rob.setMotor(0, 6000)
            rob.setMotor(1, 6000)
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
