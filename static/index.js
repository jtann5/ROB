document.addEventListener('DOMContentLoaded', function () {
    const joystick = document.getElementById('joystick');
    const container = document.getElementById('joystick-container');
    const waist = document.getElementById('waist');
    const headTilt = document.getElementById('headTilt');
    const headTurn = document.getElementById('headTurn');
    const rightShoulder = document.getElementById('rightShoulder');
    const rightBicep = document.getElementById('rightBicep');
    const rightElbow = document.getElementById('rightElbow');
    const rightForearm = document.getElementById('rightForearm');
    const rightWrist = document.getElementById('rightWrist');
    const rightClaw = document.getElementById('rightClaw');
    const leftShoulder = document.getElementById('leftShoulder');
    const leftBicep = document.getElementById('leftBicep');
    const leftElbow = document.getElementById('leftElbow');
    const leftForearm = document.getElementById('leftForearm');
    const leftWrist = document.getElementById('leftWrist');
    const leftClaw = document.getElementById('leftClaw');
    const sayBox = document.getElementById('sayBox');
    const gsayBox = document.getElementById('gsayBox');


    var dragging = false;

    // Function to handle joystick movement
    function moveJoystick(event) {
        if (dragging) {
            event.preventDefault();
            // Get x and y of user mouse or touch
            var rect = container.getBoundingClientRect();
            var x, y;
            if (event.type === 'touchmove' || event.type === 'touchstart') {
                x = event.touches[0].clientX - rect.left;
                y = event.touches[0].clientY - rect.top;
            } else {
                x = event.clientX - rect.left;
                y = event.clientY - rect.top;
            }

            // Limit the joystick to inside the container
            var dx = x - rect.width / 2;
            var dy = y - rect.height / 2;
            var distance = Math.sqrt(dx * dx + dy * dy);
            if (distance > rect.width / 2) {
                var angle = Math.atan2(dy, dx);
                x = rect.width / 2 + (rect.width / 2) * Math.cos(angle);
                y = rect.height / 2 + (rect.height / 2) * Math.sin(angle);
            }

            // Set joystick x and y
            joystick.style.top = y + 'px';
            joystick.style.left = x + 'px';

            // Get the offset of the joystick handle from the center
            var offsetX = x - rect.width / 2;
            var offsetY = y - rect.height / 2;

            // Now you can use offsetX and offsetY as needed
            console.log('Offset X:', offsetX, 'Offset Y:', offsetY);

            // IDK how do math
            leftMotorVal = 6000 - offsetY*13;
            rightMotorVal = 6000 + offsetY*13;
            setMotor(0, leftMotorVal);
            setMotor(1, rightMotrVal);
        }
    }

    function startDragging(event) {
        event.preventDefault();
        dragging = true;
        moveJoystick(event);
    }

    function endDragging() {
        dragging = false;
        joystick.style.top = '50%';
        joystick.style.left = '50%';

        // Stop robot
        setMotor(0, 6000);
        setMotor(1, 6000);
    }

    // Add event listeners for mouse and touch events
    container.addEventListener('mousedown', startDragging);
    container.addEventListener('touchstart', startDragging);

    document.addEventListener('mousemove', moveJoystick);
    document.addEventListener('touchmove', moveJoystick);

    document.addEventListener('mouseup', endDragging);
    document.addEventListener('touchend', endDragging);

    // Add event listeners for sliders
    waist.addEventListener('input', () => setMotor(2, (6000+waist.value*200)));
    headTilt.addEventListener('input', () => setMotor(3, (6000+headTilt.value*200)));
    headTurn.addEventListener('input', () => setMotor(4, (6000+headTurn.value*200)));
    rightShoulder.addEventListener('input', () => setMotor(5, (6000 + rightShoulder.value * 200)));
    rightBicep.addEventListener('input', () => setMotor(6, (6000 + rightBicep.value * 200)));
    rightElbow.addEventListener('input', () => setMotor(7, (6000 + rightElbow.value * 200)));
    rightForearm.addEventListener('input', () => setMotor(8, (6000 + rightForearm.value * 200)));
    rightWrist.addEventListener('input', () => setMotor(9, (6000 + rightWrist.value * 200)));
    rightClaw.addEventListener('input', () => setMotor(10, (6000 + rightClaw.value * 200)));
    leftShoulder.addEventListener('input', () => setMotor(11, (6000 + leftShoulder.value * 200)));
    leftBicep.addEventListener('input', () => setMotor(12, (6000 + leftBicep.value * 200)));
    leftElbow.addEventListener('input', () => setMotor(13, (6000 + leftElbow.value * 200)));
    leftForearm.addEventListener('input', () => setMotor(14, (6000 + leftForearm.value * 200)));
    leftWrist.addEventListener('input', () => setMotor(15, (6000 + leftWrist.value * 200)));
    leftClaw.addEventListener('input', () => setMotor(16, (6000 + leftClaw.value * 200)));

    // Code for keyboard control
    document.addEventListener('keydown', function(event) {
        // If the target of the event is an input element, return early
        if (event.target.tagName.toLowerCase() === 'input') {
            return;
        }

        const key = event.key.toLowerCase();
        const commandMapping = {
            'w': 'forward',
            'a': 'left',
            's': 'backward',
            'd': 'right',
            'q': 'stop',
            'p': 'waistRight',
            'o': 'waistLeft',
            'l': 'headRight',
            'k': 'headLeft',
            'm': 'headUp',
            'n': 'headDown'
        };

        if (commandMapping.hasOwnProperty(key)) {
            const command = commandMapping[key];
            sendCommandToFlask(command);
        }
    });

    // Text box event listeners
    sayBox.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            say(sayBox.value);
        } else if (event.key === '\\') {
            sayBox.value = "";
        }
    });

    gsayBox.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            gsay(gsayBox.value);
        } else if (event.key === '\\') {
            gsayBox.value = "";
        }
    });

});

function setMotor(motor, value) {
    var data = {
        motor: motor,
        value: value
    };

    fetch('/setmotor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // Convert data to JSON format
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Handle successful response
        console.log('Motor values sent successfully');
    })
    .catch(error => {
        // Handle errors
        console.error('Error sending motor values:', error);
    });
}

function sendCommandToFlask(command) {
    fetch('/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({command: command}),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function say(text) {
    if (text !== "") {
        fetch('/say', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: text}) // Convert data to JSON format
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Handle successful response
            console.log('Text sent successfully');
        })
        .catch(error => {
            // Handle errors
            console.error('Error sending motor values:', error);
        });
    }
}

function gsay(text) {
    if (text !== "") {
        fetch('/gsay', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: text}) // Convert data to JSON format
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Handle successful response
            console.log('Text sent successfully');
        })
        .catch(error => {
            // Handle errors
            console.error('Error sending motor values:', error);
        });
    }
}

function defaults() {
    sendCommandToFlask('defaults');
    const sliders = document.querySelectorAll('input[type="range"]');
    for (let slider of sliders) {
        slider.value = 0;
    }
}

function sayBox() {
    var sayBox = document.getElementById('sayBox');
    var text = sayBox.value;
    say(text);
}

function gsayBox() {
    var gsayBox = document.getElementById('gsayBox');
    var text = gsayBox.value;
    gsay(text);
}

function clearSayBox() {
    var sayBox = document.getElementById('sayBox');
    sayBox.value = "";
}

function clearGsayBox() {
    var gsayBox = document.getElementById('gsayBox');
    gsayBox.value = "";
}