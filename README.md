# ROB
This is the repo for an embedded systems robotics project. Major python files and their function are discussed below.

## rob.py
rob.py contains a Rob class that is used for controlling the robots functions. This includes speech, movement, and gestures.

## AIEngine.py
Contains an AIEngine class that communicates with the OpenAI Assistants API to get responses for various inputs.

## DialogEngine.py
Contains a DialogEngine class that parses a file for rules and then gives responses for inputs.

## UWB.py

## newWebControl.py
Allows a user to access manual controls for the robot though a browser. JavaScript requests are used to issue commands to the robot. oldWebControl.py handles the same requests but using Flask instead of FastAPI.

## static/index.js
Issues requests to the server for controlling robot functions.