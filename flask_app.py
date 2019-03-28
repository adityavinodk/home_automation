from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from gpiozero import LED
from time import sleep, time
import Adafruit_DHT
import RPi.GPIO as GPIO

app = Flask(__name__)
app.secret_key = os.urandom(12)

# For LED
led = LED(18)

# For Ultrasonic Sensor
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 17
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

@app.route('/')
def home():
	if session.get('temp_humid_readings'):
		humid, temp = session['temp_humid_readings']
	if session.get('distance_readings'):
		distance = session['distance_readings']
	if not session.get('temp_humid_readings') or not session.get('distance_readings'):
		humid = None
		temp = None
		distance = None
	return render_template('home.html', humid = humid, temp = temp, distance = distance)

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

@app.route('/distance', methods=['GET'])
def distance():
	# Set trigger to High
	GPIO.output(GPIO_TRIGGER, True)
	# Set trigger to Low after some time
	sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	
	startTime = time()
	stopTime = time()
	
	while GPIO.input(GPIO_ECHO) == 0:
		startTime = time()
		
	while GPIO.input(GPIO_ECHO) == 1:
		stopTime = time()
		
	timeElapsed = stopTime - startTime
	distance = (timeElapsed * 34300) / 2
	session['distance_readings'] = distance
	return home()


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)


