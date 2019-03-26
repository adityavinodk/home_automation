from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from gpiozero import LED
from time import sleep

app = Flask(__name__)
app.secret_key = os.urandom(12)
led = LED(18)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/switch_on', methods=["GET"])
def switch_on():
	led.on()
	print("Light is on")
	return home()


@app.route('/switch_off', methods=["GET"])
def switch_off():
	led.off()
	print("Light is off")
	return home()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)


