from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from gpiozero import LED
from time import sleep
import Adafruit_DHT

app = Flask(__name__)
app.secret_key = os.urandom(12)
led = LED(18)

@app.route('/')
def home():
	if session.get('temp_humid_readings'):
		humid, temp = session['temp_humid_readings']
	else:
		humid = None
		temp = None
	return render_template('home.html', humid = humid, temp = temp)

@app.route('/switch_on', methods=["GET"])
def switch_on():
	if not session.get('light_on'):
		led.on()
		session['light_on'] = True
		print("Light is on")
		return home()


@app.route('/switch_off', methods=["GET"])
def switch_off():
	if session.get('light_on'):
		led.off()
		session['light_on'] = False
		print("Light is off")
		return home()

@app.route('/get_reading', methods=["GET"])
def get_hum_temp_reading():
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	session['temp_humid_readings'] = [humidity, temperature]
	# print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
	return home()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)


