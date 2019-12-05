'''
    ECE 4180 Final Project
    Team Name: Wide Alert
    By: Jeffrey Jacob and Shruti Ramanathan
    Fall 2019
'''
from __future__ import print_function
from twilio.rest import Client
import cv2 as cv
import argparse
import serial
import time
s = serial.Serial("/dev/ttyACM0")
global eyesLost
eyesLost = 0
EYETHRES = 0
lastAlert = time.time()
account_sid='PUT ACCOUNT SID'
auth_token='PUT AUTH TOKEN'
global client
client = Client(account_sid, auth_token)
def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    global eyesLost
    #cv.putText(frame, "Eye Lost Count: %d" % eyesLost,(10,10), cv.FONT_HERSHEY_SIMPLEX,1, (255,255,255), 2)
    print("Faces: %d" % len(faces))
    global client
    if len(faces) < 1:
        global eyesLost
        global lastAlert
        if abs(time.time() - lastAlert) > 5:
            eyesLost += 1
            print("PAY ATTENTION TO THE ROAD!")
            s.write(b'1')
            lastAlert = time.time()
        if eyesLost > 1:
            message = client.messages.create(body='John Smith\'s Wheel-Awake System detected multiple driving distractions. Consider reaching out.', from_='+12029182874', to='+17706171021')
            print("SENT SMS")
            eyesLost = 0
    else:
        if abs(time.time() - lastAlert) > 2:
                s.write(b'0')

    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        #frame = cv.ellipse(frame, center,  (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        print("Eyes: %d" % len(eyes))
        if len(eyes) < 2:
            if abs(time.time() - lastAlert) > 5:
                eyesLost += 1
                print("PAY ATTENTION TO THE ROAD!")
                s.write(b'1')
                lastAlert = time.time()
            if eyesLost > 1:
                message = client.messages.create(body='John Smith\'s Wheel-Awake System detected multiple driving distractions. Consider reaching out.', from_='+12029182874', to='+17706171021')
                print("SENT SMS")
                eyesLost = 0
        else:
            if abs(time.time() - lastAlert) > 2:
                s.write(b'0')
            #for (x2,y2,w2,h2) in eyes:
             #   eye_center = (x + x2 + w2//2, y + y2 + h2//2)
              #  radius = int(round((w2 + h2)*0.25))
               # frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    #cv.imshow('Capture - Face detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='/home/pi/Desktop/4180final/finalproj/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='/home/pi/Desktop/4180final/finalproj/lib/python3.7/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if  not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    _, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    #time.sleep(0.1)
    if cv.waitKey(10) == 27:
        break
