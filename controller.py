# Python code for controller native service - controller.py

import os
import time
import datetime
import MySQLdb
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from stream import live_stream, kill_stream
from mailer import email

GPIO.setmode(GPIO.BCM)
ROOM_SENSOR_PIN = 27
DOOR_SENSOR_PIN = 23
BLED_PIN = 16
GLED_PIN = 20
RLED_PIN = 21
GGLED_PIN = 26
GPIO.setup(ROOM_SENSOR_PIN, GPIO.IN)
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RLED_PIN, GPIO.OUT)
GPIO.setup(BLED_PIN, GPIO.OUT)
GPIO.setup(GLED_PIN, GPIO.OUT)
GPIO.setup(GGLED_PIN, GPIO.OUT)
GPIO.output(GGLED_PIN, False)
GPIO.output(RLED_PIN, False)
GPIO.output(BLED_PIN, False)
GPIO.output(GLED_PIN, False)

check_stream = 0
check_door = 0

# Get current mode from DB
def getCurrentMode():
    db = MySQLdb.connect("localhost", "root", "stevens123", "scc")
    curs=db.cursor()
    curs.execute('SELECT * FROM myapp_mode')
    data = curs.fetchone()  # (1, u'auto')
    return data[1]

# Get current action from DB
def getCurrentAction():
    db = MySQLdb.connect("localhost", "root", "stevens123", "scc")
    curs=db.cursor()
    curs.execute('SELECT * FROM myapp_action')
    data = curs.fetchone()  # (1, u'on')
    return data[1]

# Update current action in DB
def setCurrentAction(val):
    db = MySQLdb.connect("localhost", "root", "stevens123", "scc")
    curs=db.cursor()
    query = 'UPDATE myapp_action set name = "'+val+'"'
    curs.execute(query)
    db.commit()
    #con.close()

def insert_motion():
    db = MySQLdb.connect("localhost", "root", "stevens123", "scc")
    curs=db.cursor()
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    motion_type = 'Auto Mode'
    curs.execute ("INSERT INTO myapp_motion(motion_type,motion_date) values(%s,%s)",(motion_type,timestamp))
    db.commit()
    print "Data committed" + "\n"

def insert_door():
    db = MySQLdb.connect("localhost", "root", "stevens123", "scc")
    curs=db.cursor()
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    door_type = 'Auto Mode'
    curs.execute ("INSERT INTO myapp_door(door_type,door_date) values(%s,%s)",(door_type,timestamp))
    db.commit()
    print "Data committed" + "\n"

def take_pic():
    global check_stream
    kill_stream()
    check_stream = 0
    setCurrentAction('off')
    time.sleep(0.5)
    camera = PiCamera()
    camera.capture('/home/pi/scc/myapp/static/myapp/pic.jpg')
    print "Snapshot Saved"
    camera.close()
    
def take_vid(time_to_record):
    kill_stream()
    check_stream = 0
    setCurrentAction('off')
    time.sleep(0.5)
    camera = PiCamera()
    camera.start_recording('my_video.h264')
    camera.wait_recording(time_to_record)
    camera.stop_recording()
    print "Recording Saved"
    camera.close()
    
def stream():
    global check_stream
    
    if check_stream==0:
        setCurrentAction('stream')
        live_stream('1080','720')
        check_stream =1
    else:
        pass

def readingRoomSensor():
    print "Check motion"
    if GPIO.input(ROOM_SENSOR_PIN):
        print 'Motion Detected'
        GPIO.output(BLED_PIN, True)
        return 1
    else:
        GPIO.output(BLED_PIN, False)
        return 0

def readingDoorSensor():
    print "Checking Door Status"
    if GPIO.input(DOOR_SENSOR_PIN):
        print 'Door Opened'
        GPIO.output(GGLED_PIN, True)
        return 1
    else:
        GPIO.output(GGLED_PIN, False)
        return 0

def runManualMode():
    global check_stream
    print "\nManual Mode Running..."
    currentAction = getCurrentAction()

    if currentAction == 'snap':
        take_pic()
        print 'Snapshot Saved'
        #setCurrentAction('off')
        #check_stream =0
        
    elif currentAction == 'vid':
        print "Recording"
        take_vid(5)
        print 'Video Recorded for 5 seconds'
        #setCurrentAction('off')
        #check_stream =0
        
    elif currentAction == 'stream':
        print "Streaming"
        stream()
        #setCurrentAction('off')
        
    elif currentAction == 'off':
        print "Waiting for user"
        kill_stream()
        check_stream =0
        
def runAutoMode():
        print "\nAuto Mode Running..."
        setCurrentAction('off')
        global check_stream
        global check_door
        roomState = readingRoomSensor()

        if roomState == True:
            insert_motion()
            take_pic()
        
        doorState = readingDoorSensor()

        if doorState == True:
            if check_door ==0:
                insert_door()
                print "Email sending.."
                email('tahmad@stevens.edu')
                print "Email sent"
                print "Check stream..."
                stream()
                check_door =1
            elif check_stream ==0:
                stream()
            else:
                pass
        else:
            kill_stream()
            setCurrentAction('off')
            check_stream = 0
            check_door = 0

# Controller main function
def runController():
    currentMode = getCurrentMode()
    if currentMode == 'auto':
        runAutoMode()
    elif currentMode == 'manual':
        runManualMode()
    return True

while True:
    try:
        runController()
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        kill_stream()
        exit()
