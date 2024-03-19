import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from rob import get_rob_instance

rob = get_rob_instance()
rob.defaults()
face = rob.face

forward_backward = 0
waist_value = 0
head_left_right_value = 0
head_up_down_value = 0
left_right = 0

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/mainmotors')
async def mainmotors(request: Request):
    data = await request.json()
    motor0 = int(data.get("motor0"))
    motor1 = int(data.get("motor1"))
    rob.setMotor(0, motor0)
    rob.setMotor(1, motor1)

    response_data = {'status': 'success'}
    return response_data


@app.post('/setmotor')
async def setmotor(request: Request):
    data = await request.json()
    motor = int(data.get("motor"))
    value = int(data.get("value"))
    rob.setMotor(motor, value)

    response_data = {'status': 'success'}
    return response_data


@app.post('/say')
async def say(request: Request):
    data = await request.json()
    text = data.get("text")
    rob.say(text)
    if (text == "rizz mode activated"):
        rob.rizz()

    response_data = {'status': 'success'}
    return response_data


@app.post('/gsay')
async def gsay(request: Request):
    data = await request.json()
    text = data.get("text")
    rob.gsay(text)
    if (text == "rizz mode activated"):
        rob.rizz()

    response_data = {'status': 'success'}
    return response_data


@app.post('/command')
async def command(request: Request):
    global forward_backward, waist_value, head_left_right_value, head_up_down_value, left_right

    data = await request.json()
    command = data.get("command")

    if command == 'defaults':
        rob.defaults()
    elif command == 'forward':
        forward_backward += 1
    elif command == 'backward':
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
    if (face.robot_state != "moving") and (rightmotor != 6000) and (leftmotor != 6000):
        app.queue.put("moving")
    elif (rightmotor == 6000) and (leftmotor == 6000):
        app.queue.put("idle")
    setValues(leftmotor, rightmotor, waist, head_vertical, head_horizontal)

    # set all the amounts
    response_data = {'status': 'success'}
    return response_data

def setValues(leftmotor, rightmotor, waist, head_vertical, head_horizontal):
    rob.setMotor(0, leftmotor)
    rob.setMotor(1, rightmotor)
    rob.setMotor(2, waist)
    rob.setMotor(3, head_vertical)
    rob.setMotor(4, head_horizontal)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9000)

