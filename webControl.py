from flask import Flask, render_template, send_from_directory, jsonify, request, Blueprint, redirect
import os
from rob import ROB

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'), static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True, host="0.0.0.0", port=5000)