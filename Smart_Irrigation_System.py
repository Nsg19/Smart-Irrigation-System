import RPi.GPIO as gpio
import Adafruit_DHT
import sys
import time
import string
import threading
import os

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

sensor=Adafruit_DHT.DHT11
dht=17

rain=27
gpio.setup(27,gpio.IN)

soil=22
gpio.setup(22,gpio.IN)

motor_n1=14
motor_n2=15
en=18
gpio.setup(18,gpio.OUT)
gpio.setup(14,gpio.OUT)
gpio.setup(15,gpio.OUT)

trig=23
echo=24
gpio.setup(23,gpio.OUT)
gpio.setup(24,gpio.IN)
gpio.output(23,False)

gpio.setup(21,gpio.OUT)

humidity=0

def dht():
    print("\nInitializing DHT sensor...\n")
    time.sleep(2)
    while True:
        global humidity
        humidity, temperature=Adafruit_DHT.read_retry(11,17)
        if humidity is not None and temperature is not None:
            print('Temp:{0:0.1f}*C Humidity: {1:0.1f}%'.format(temperature,humidity))
            time.sleep(0.2)
        else:
            print("\nFailed to get reading...\n")

def rain():
    print("\nInitializing Rain Sensor...\n")
    time.sleep(2)
    while True:
        if (gpio.input(27)==False):
            print("Raining")
            time.sleep(0.2)
        else:
            print("Not raining")
            time.sleep(0.2)

def soil():
    print("\nInitializing Soil Moisture Sensor...\n")
    time.sleep(2)
    while 1:
        if (gpio.input(22)==False):
            print("Wet Soil")
            time.sleep(0.2)
            
        else:
            print("Dry Soil")
            time.sleep(0.2)

def motor():
    print("\nInitializing Motor...\n")
    time.sleep(2)
    while True:
        if(gpio.input(22)==True and gpio.input(27)==True and humidity<60):
            gpio.output(18,True)
            gpio.output(14,True)
            gpio.output(15,False)
            print("motor on")
            time.sleep(1)
        else:
            time.sleep(2)
            gpio.output(14,False)
            gpio.output(15,False)
            print("motor off")
            

def ultrasonic():
    print("\nInitializing Ultrasonic Sensor...\n")
    global distance
    time.sleep(2)
    while True:
        time.sleep(1)
        gpio.output(trig,True)
        time.sleep(0.00001)
        gpio.output(trig,False)

        while gpio.input(echo)==0:
            pulse_start=time.time()

        while gpio.input(echo)==1:
            pulse_end=time.time()

        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance,2)
        print("Distance",distance,"cm")
        if(distance>13):
            gpio.output(21,True)
            time.sleep(0.5)
            gpio.output(21,False)


print("\n====================== Starting ======================\n")
print("\nInitializing the system...\n")
time.sleep(5)
print("\nSystem is Ready\n")
time.sleep(2)
try:
    while True:
        t1=threading.Thread(target=dht)
        t2=threading.Thread(target=rain)
        t3=threading.Thread(target=soil)
        t4=threading.Thread(target=motor)
        t5=threading.Thread(target=ultrasonic)
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
except KeyboardInterrupt:
    print("\n\nForcely Stop System\n\n")
    time.sleep(4)
    gpio.cleanup()
    time.sleep(1)

