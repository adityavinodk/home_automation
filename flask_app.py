from flask import Flask, redirect, render_template, session
import os
from gpiozero import LED
import simplejson as json
from time import sleep, time
import Adafruit_DHT
import RPi.GPIO as GPIO

app = Flask(__name__)
app.secret_key = os.urandom(12)

# For system LED's
led = LED(18)
led1 = LED(10)
led2 = LED(9)

# For Ultrasonic Sensor
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 17
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# For Buzzer
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)

@app.route('/')
def options():
	humid, temp = get_hum_temp_reading()
	return render_template('options.html', humid = humid, temp = temp)

@app.route('/home')
def home():
	danger = None
	if session.get('system'):
		dist = distance()
		if int(dist) < 10:
			danger=True
			GPIO.output(22, GPIO.HIGH)
			sleep(1)
			GPIO.output(22, GPIO.LOW)
		else: GPIO.output(22, GPIO.LOW)
		return render_template('home.html', dist=dist, danger=danger)
	return redirect('/')

@app.route('/switch_on_system', methods=["GET"])
def switch_on():
	session['system']=True
	led.on()
	return redirect('/home')


@app.route('/switch_off_system', methods=["GET"])
def switch_off():
	session['system']=False
	led.off()
	return redirect('/')
	
@app.route('/switch_on_light/<pos>', methods=["GET"])
def light_on(pos):
	if pos=='10':
		if not session.get('led1'):
			led1.on()
			session['led1']=True
	elif pos=='9':
		if not session.get('led2'):
			led2.on()
			session['led2']=True
	return redirect('/')
	
@app.route('/switch_off_light/<pos>', methods=["GET"])
def light_off(pos):
	if pos=='10':
		if session.get('led1'):
			led1.off()
			session['led1']=False
	elif pos=='9':
		if session.get('led2'):
			led2.off()
			session['led2']=False
	return redirect('/')

@app.route('/hum_temp')
def get_hum_temp_reading():
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	session['temp_humid_readings'] = True
	# print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
	return [humidity, temperature]

@app.route('/distance')
def distance():
	# Set trigger to High
	GPIO.output(GPIO_TRIGGER, True)
	# Set trigger to Low after some time
	sleep(0.000001)
	GPIO.output(GPIO_TRIGGER, False)

	startTime = time()
	stopTime = time()

	while GPIO.input(GPIO_ECHO) == 0:
		startTime = time()

	while GPIO.input(GPIO_ECHO) == 1:
		stopTime = time()

	timeElapsed = stopTime - startTime
	distance = (timeElapsed * 34300) / 2
	session['distance_readings'] = True
	return distance

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)


