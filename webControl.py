from flask import Flask, render_template, send_from_directory, jsonify, request, Blueprint, redirect
import os
from rob import ROB

rob = ROB()
rob.defaults()

def setValues(leftmotor, rightmotor, waist, head_vertical, head_horizontal):
    rob.setMotor(0, leftmotor)
    rob.setMotor(1, rightmotor)
    rob.setMotor(2, waist)
    rob.setMotor(3, head_vertical)
    rob.setMotor(4, head_horizontal)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'), static_folder='static')

forward_backward = 0
waist_value = 0
head_left_right_value = 0
head_up_down_value = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    global forward_backward, waist_value, head_left_right_value, head_up_down_value

    data = request.get_json()
    command = data.get("command")

    if command == 'forward':
        forward_backward += 1
    elif command ==  'backward':
        forward_backward -= 1
    elif command == 'left':
        # handle left
        # turn left here
        pass
    elif command == 'right':
        # handle right
        # turn right here
        pass
    elif command == 'stop':
        # handle stop
        # make stop function?
        pass
    elif command == 'waistRight':
        waist_value += 1
    elif command == 'waistLeft':
        waist_value -= 1
    elif command == 'headRight':
        head_left_right_value += 1
    elif command == 'headLeft':
        head_left_right_value -= 1
    elif command == 'headUp':
        head_up_down_value += 1
    elif command == 'headDown':
        head_up_down_value -= 1

    if forward_backward > 3:
        forward_backward = 3
    if forward_backward < -3:
        forward_backward = -3
    if waist_value > 5:
        waist_value = 5
    if waist_value < -5:
        waist_value = -5
    if head_left_right_value > 5:
        head_left_right_value = 5
    if head_left_right_value < -5:
        head_left_right_value = -5
    if head_up_down_value > 5:
        head_up_down_value = 5
    if head_up_down_value < -5:
        head_up_down_value = -5

    default = 6000
    rightmotor = default + (300 * forward_backward)
    leftmotor = default - (300 * forward_backward)
    waist = default + (200 * waist_value)
    head_vertical = default + (200 * head_up_down_value)
    head_horizontal = default + (200 * head_left_right_value)

    setValues(leftmotor, rightmotor, waist, head_vertical, head_horizontal)

    # set all the amounts
    response_data = {'status': 'success'}
    return jsonify(response_data)


@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    joystickX = data.get("joystickX")
    joystickY = data.get("joystickY")
    slider1 = data.get('slider1')
    slider2 = data.get('slider2')
    slider3 = data.get('slider3')

    firstValL = 6000
    firstValR = 6000

    if joystickX > 0:
        firstValL = 6000 + (200 * joystickX)
    if joystickX < 0:
        firstValR = 6000 - (200 * joystickX)

    secondValL = 6000 - (200 * joystickY)
    secondValR = 6000 + (200 * joystickY)

    rightVal = (firstValL + secondValL) / 2
    leftVal = (firstValR + secondValR) / 2

    setValues(int(leftVal), int(rightVal), 6000-int(slider1)*200, 6000-int(slider2)*200, 6000-int(slider3)*200)

    response_data = {'status': 'success'}
    return jsonify(response_data)

def getWheelsValue(value):
    print("v", str(value))
    return str(value)

app.run(debug=True, host="0.0.0.0", port=5000)