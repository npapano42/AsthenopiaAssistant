import numpy as np
import cv2
import sys
import os
import datetime as dt

# EAR = eye aspect ratio
# to store in list:
# index 0 is datetime timestamp for start
# index 1 is blink counter
# all others are ordered lists:
# EAR (number 0-1)
# timestamp offset from start
# boolean isDetectingFace
# boolean isDetectingEyes

face_cascade = cv2.CascadeClassifier('venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('venv/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
start_time = dt.datetime.now()

frame_num = 0

time_list = [start_time.strftime('%m/%d/%Y %H:%M')]

if cap is None:
    print('no vid')
    sys.exit(0)

font = cv2.FONT_HERSHEY_SIMPLEX
text_loc = (10, 35)

# for centering eyes
face_offset_size = 30

while True:
    ret, img = cap.read()
    frame_num += 1
    if img is None:
        print('video ended')
        sys.exit(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    timestamp = str(dt.datetime.now() - start_time)
    is_detecting_face = False
    is_detecting_eyes = False
    for (x, y, w, h) in faces:
        is_detecting_face = True
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, minNeighbors=8, minSize=(10, 10), maxSize=(50, 50))
        if time_list[-1] != frame_num:
            time_list.append([frame_num, timestamp])
        for (ex, ey, ew, eh) in eyes:
            is_detecting_eyes = True
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
    cv2.putText(img, 'Timestamp: ' + timestamp +
                ", face detecting: " + str(is_detecting_face) +
                ", eyes detecting: " + str(is_detecting_eyes),
                text_loc, font,
                1, (255, 255, 255), 2)
    cv2.imshow('img', img)

    # slice last byte and check if key pressed is esc
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

for i in time_list:
    print(i)

