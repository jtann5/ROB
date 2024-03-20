from flask import Flask, render_template, send_from_directory, jsonify, request, Blueprint, redirect
import os
import multiprocessing
from rob import ROB

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'), static_folder='static')

forward_backward = 0
waist_value = 0
head_left_right_value = 0
head_up_down_value = 0
left_right = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mainmotors', methods=['POST'])
def mainmotors():
    data = request.get_json()
    motor0 = int(data.get("motor0"))
    motor1 = int(data.get("motor1"))
    rob.setMotor(0, motor0)
    rob.setMotor(1, motor1)

    response_data = {'status': 'success'}
    return jsonify(response_data)

@app.route('/setmotor', methods=['POST'])
def setmotor():
    data = request.get_json()
    motor = int(data.get("motor"))
    value = int(data.get("value"))
    rob.setMotor(motor, value)

    response_data = {'status': 'success'}
    return jsonify(response_data)

@app.route('/say', methods=['POST'])
def say():
    data = request.get_json()
    text = data.get("text")
    rob.say(text)

    response_data = {'status': 'success'}
    return jsonify(response_data)

@app.route('/gsay', methods=['POST'])
def gsay():
    data = request.get_json()
    text = data.get("text")
    rob.gsay(text)

    response_data = {'status': 'success'}
    return jsonify(response_data)

@app.route('/command', methods=['POST'])
def command():
    global forward_backward, waist_value, head_left_right_value, head_up_down_value, left_right

    data = request.get_json()
    command = data.get("command")

    if command == 'defaults':
        rob.defaults()
    elif command == 'forward':
        forward_backward += 1
    elif command ==  'backward':
        forward_backward -= 1
    elif command == 'left':
        left_right += 1
    elif command == 'right':
        left_right -= 1
    elif command == 'stop':
        forward_backward = 0
        waist_value = 0
        head_left_right_value = 0
        head_up_down_value = 0
        left_right = 0
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
    if left_right > 3:
        forward_backward = 3
    if left_right < -3:
        forward_backward = -3

    default = 6000
    rightmotor = default + (280 * forward_backward) + (280 * left_right)
    leftmotor = default - (300 * forward_backward) + (300 * left_right)
    waist = default + (200 * waist_value)
    head_vertical = default + (200 * head_up_down_value)
    head_horizontal = default + (200 * head_left_right_value)

    setValues(leftmotor, rightmotor, waist, head_vertical, head_horizontal)

    # set all the amounts
    response_data = {'status': 'success'}
    return jsonify(response_data)

rob = ROB()
rob.defaults()

def setValues(leftmotor, rightmotor, waist, head_vertical, head_horizontal):
    rob.setMotor(0, leftmotor)
    rob.setMotor(1, rightmotor)
    rob.setMotor(2, waist)
    rob.setMotor(3, head_vertical)
    rob.setMotor(4, head_horizontal)
    
def run_flask():
    app.run(debug=True, host="0.0.0.0", port=9000)

def run_face():
    rob.defaults()

    rob.face.mainloop()

run_flask()

# if __name__ == "__main__":
#     rob = ROB()
#     rob.defaults()

#     flask_process = multiprocessing.Process(target=run_flask)
#     flask_process.start()

#     rob.face.mainloop()

#     flask_process.join()
    
# if __name__ == "__main__":
#     face_process = multiprocessing.Process(target=run_face)
#     face_process.start()

#     run_flask()

#     face_process.join()