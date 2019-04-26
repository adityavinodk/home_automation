# Home Automation Project using Raspberry Pi
This project is implemented using Raspberry Pi and the web application using Flask. The Raspberry Pi is connected to several LED’s, which can be switched on and off using buttons on the website. The temperature and humidity DHT11 sensor takes its readings and the values are constantly updated on the website. When the security system is enabled, an Ultrasonic sensor is used to detect any movement, with small distance readings triggering a buzzer.

For setting up the Raspberry Pi - 
1. Connect 3 LED's to `ports 18, 10 and 9` 
2. For connecting the Ultrasonic sensor, connect `Trigger pin to port 17` and `Echo pin to port 24`
3. Connect `buzzer to port 22`
4. Connect Temperature and Humidity sensor - `DHT11 to port 4`
5. Connect Ground and 5V ports to the breadboard

For starting the Flask server - 
1. SSH into the raspberry pi
2. Go to the root folder and run the python file - 
```shell
python3 flask_app.py
```
3. Type `ifconfig` terminal to get the Private IP of the Pi and type 
```shell
<PrivateIP>:5000
``` 
on the browser to start the application. To change the IP or port, edit `Line 114 in flask_app.py`

This project mimics Home Automation system which enables users to fully control their home appliances like turning on lights in different rooms, checking the surrounding temperature and humidity, and enabling a security system which detects movement. This project can be scaled to automate more home appliances with different use cases, add a camera module to the security system for human detection etc.
