import numpy as np
import cv2
import sys
import datetime as dt
import dlib
import math

# TODO: add to EAR_data the ordered pairs correcrtly

# EAR = eye aspect ratio
# to store in list:
# index 0 is datetime timestamp for start
# index 1 is blink counter
# all others are ordered lists:
# EAR (number 0-1)
# timestamp offset from start
# boolean isDetectingEyes

# detector/predictor for face/eyes
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# font for displaying telemetry
font = cv2.FONT_HERSHEY_SIMPLEX
text_loc = (10, 35)

# start video capture
cap = cv2.VideoCapture(0)
start_time = dt.datetime.now()
frame_num = 0

# time list is the data array
EAR_data = [start_time.strftime('%m/%d/%Y %H:%M')]

# cancel on no webcam
if cap is None:
    print('no video')
    sys.exit(0)

# loop for EAR detection
while True:
    # set up frame for analysis
    ret, img = cap.read()

    if img is None:
        print('video ended')
        sys.exit(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    EAR = -1
    # set up telemetry
    timestamp = str(dt.datetime.now() - start_time)
    is_detecting_eyes = False
    frame_num += 1

    # face analysis
    faces = detector(gray)
    for face in faces:
        # 36 - 47 are the landmarks for the eyes
        landmarks = predictor(gray, face)

        # compute EAR from left eye (reference: png file)
        upper_eye = (int((landmarks.part(37).x + landmarks.part(38).x)/2), int((landmarks.part(37).y + landmarks.part(38).y)/2))
        lower_eye = (int((landmarks.part(40).x + landmarks.part(41).x)/2), int((landmarks.part(40).y + landmarks.part(41).y)/2))
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(39).x, landmarks.part(39).y)
        # ratio of distances

        vert_len = math.sqrt(math.pow(upper_eye[0]-lower_eye[0], 2) + math.pow(upper_eye[1]-lower_eye[1], 2))
        horiz_len = math.sqrt(math.pow(left_eye[0]-right_eye[0], 2) + math.pow(left_eye[1]-right_eye[1], 2))
        EAR = round(vert_len/horiz_len, 2)
        EAR_data.append(EAR)
        # on screen eye telemetry
        cv2.line(img, upper_eye, lower_eye, (255, 0, 0), 2)
        cv2.line(img, left_eye, right_eye, (255, 0, 0), 2)
        for n in range(36, 48):
            is_detecting_eyes = True
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            # dot each landmark
            cv2.circle(img, (x, y), 4, (255, 255, 255), -1)

    telemetry = 'Timestamp: ' + timestamp \
                + ', eyes detecting: ' \
                + str(is_detecting_eyes)

    if is_detecting_eyes:
        telemetry += ', EAR: ' + str(EAR)

    # display telemetry
    cv2.putText(img, telemetry,
                text_loc, font,
                1, (255, 255, 255), 2)

    # show frame
    cv2.imshow('img', img)

    # slice last byte and check if key pressed is esc
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

for i in EAR_data:
    print(i)

