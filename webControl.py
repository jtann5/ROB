from flask import Flask, render_template, send_from_directory, jsonify, request, Blueprint, redirect
import os
# from rob import ROB

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'), static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

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

    leftVal = (firstValL + secondValL) / 2
    rightVal = (firstValR + secondValR) / 2

    print("Joystick X: " + str(joystickX))
    print("Joystick Y: " + str(joystickY))
    print(slider1, slider2, slider3)
    print(leftVal, rightVal)

    response_data = {'status': 'success'}
    return jsonify(response_data)

def getWheelsValue(value):
    print("v", str(value))
    return str(value)

app.run(debug=True, host="0.0.0.0", port=5000)