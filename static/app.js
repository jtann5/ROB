document.addEventListener('DOMContentLoaded', function () {
    const joystick = document.getElementById('joystick');
    const slider1 = document.getElementById('slider1');
    const joystickContainter = document.getElementById('joystick-container');
    const slider2 = document.getElementById('slider2');
    const slider3 = document.getElementById('slider3');

    let isDragging = false;

    joystick.addEventListener('mousedown', (event) => {
        event.preventDefault();

        // Calculate initial offset from the center
        const containerRect = document.getElementById('joystick-container').getBoundingClientRect();
        const centerX = containerRect.left + containerRect.width / 2;
        const centerY = containerRect.top + containerRect.height / 2;

        const initialOffsetX = event.clientX - centerX;
        const initialOffsetY = event.clientY - centerY;

        isDragging = true;
        updateJoystickValues();  // Update joystick values on click


        document.addEventListener('mousemove', moveListener);
    });

    document.addEventListener('keydown', function(event) {
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

    document.addEventListener('keyup', function(event) {
       // handle key release if needed
    });

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


function moveListener(event) {
    if (isDragging) {
        const containerRect = document.getElementById('joystick-container').getBoundingClientRect();
        const centerX = containerRect.left + containerRect.width / 2;
        const centerY = containerRect.top + containerRect.height / 2;

        const mouseX = event.clientX;
        const mouseY = event.clientY;

        const angle = Math.atan2(mouseY - centerY, mouseX - centerX);
        const distance = Math.min(containerRect.width / 2, Math.hypot(mouseY - centerY, mouseX - centerX));

        const clampedX = centerX + distance * Math.cos(angle);
        const clampedY = centerY + distance * Math.sin(angle);

        joystick.style.left = clampedX - containerRect.left - joystick.offsetWidth / 2 + 'px';
        joystick.style.top = clampedY - containerRect.top - joystick.offsetHeight / 2 + 'px';

        updateJoystickValues();  // Update joystick values while dragging
    }
}







    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            resetJoystick();  // Reset joystick values on release
            document.removeEventListener('mousemove', moveListener);
        }
    });



    const updateJoystickValues = () => {
        const joystickX = parseFloat(joystick.style.left) / (document.getElementById('joystick-container').offsetWidth - joystick.offsetWidth) * 20 - 10;
        const joystickY = parseFloat(joystick.style.top) / (document.getElementById('joystick-container').offsetHeight - joystick.offsetHeight) * 20 - 10;

        console.log("Joystick X for movement:", joystickX);
        console.log("Joystick Y for movement:", joystickY);

        // Send data to Flask server
        sendDataToFlask(joystickX, joystickY, slider1.value, slider2.value, slider3.value);
    };

    const resetJoystick = () => {
        const containerRect = document.getElementById('joystick-container').getBoundingClientRect();
        //joystick.style.left = containerRect.width / 2 - joystick.offsetWidth / 2 + 'px';
        //joystick.style.top = containerRect.height / 2 - joystick.offsetHeight / 2 + 'px';
        const centerX = (joystick-container.clientWidth - joystick.clientWidth) / 2;
        const centerY = (joystick-container.clientHeight - joystick.clientHeight) / 2;

        joystick.style.left = '${centerX}px';
        joystick.style.top = '${centerY}px';
        // Update sliders to default values
        //slider1.value = 0;
        //slider2.value = 0;

        

        // Send data to Flask server
        sendDataToFlask(0, 0, slider1.value, slider2.value, slider3.value);
    };

    const sendDataToFlask = (joystickX, joystickY, slider1Value, slider2Value, slider3Value) => {
        const slidersData = {
            joystickX: joystickX,
            joystickY: joystickY,
            slider1: slider1Value,
            slider2: slider2Value,
            slider3: slider3Value,
        };

        // Send data to Flask server
        fetch('/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(slidersData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    // Slider change event
    slider1.addEventListener('input', () => sendDataToFlask(0, 0, slider1.value, slider2.value, slider3.value));
    slider2.addEventListener('input', () => sendDataToFlask(0, 0, slider1.value, slider2.value, slider3.value));
    slider3.addEventListener('input', () => sendDataToFlask(0, 0, slider1.value, slider2.value, slider3.value));

    // Initial update when the page loads
    sendDataToFlask(0, 0, slider1.value, slider2.value, slider3.value);
});