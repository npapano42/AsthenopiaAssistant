import numpy as np
import cv2
import sys
import datetime as dt
import dlib
import math
import matplotlib

# TODO: add to EAR_data the ordered pairs correctly
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

# time list is the data array
start_time = dt.datetime.now().strftime('%m/%d/%Y %H:%M')
EAR_data = [start_time, 0, 0]

# cancel on no webcam
if cap is None:
    print("Can't start, no webcam detected! Aborting...")
    sys.exit(0)


start_blink = False


def check_blink(ear):
    global start_blink
    if ear < ear_threshold:
        start_blink = True

    if ear > ear_threshold and start_blink is True:
        start_blink = False
        EAR_data[2] += 1


def face_analysis():
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    EAR = -1
    # set up telemetry
    timestamp = str(dt.datetime.now())[11:]
    is_detecting_eyes = False
    # face analysis
    faces = detector(gray)
    for face in faces:
        # 36 - 47 are the landmarks for the eyes
        landmarks = predictor(gray, face)

        # compute EAR from left eye (reference: png file)
        upper_eye = (
            int((landmarks.part(37).x + landmarks.part(38).x) / 2),
            int((landmarks.part(37).y + landmarks.part(38).y) / 2))
        lower_eye = (
            int((landmarks.part(40).x + landmarks.part(41).x) / 2),
            int((landmarks.part(40).y + landmarks.part(41).y) / 2))
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(39).x, landmarks.part(39).y)
        # ratio of distances

        vert_len = math.sqrt(math.pow(upper_eye[0] - lower_eye[0], 2) + math.pow(upper_eye[1] - lower_eye[1], 2))
        horiz_len = math.sqrt(math.pow(left_eye[0] - right_eye[0], 2) + math.pow(left_eye[1] - right_eye[1], 2))
        EAR = round(vert_len / horiz_len, 2)

        check_blink(EAR)

        # on screen eye telemetry
        cv2.line(img, upper_eye, lower_eye, (255, 0, 0), 2)
        cv2.line(img, left_eye, right_eye, (255, 0, 0), 2)
        for n in range(36, 48):
            is_detecting_eyes = True
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            # dot each landmark
            cv2.circle(img, (x, y), 4, (255, 255, 255), -1)

    # generate and display telemetry
    telemetry = 'Timestamp: ' + timestamp \
                + ', blinks: ' + str(EAR_data[2]) \
                + ', eyes detecting: ' \
                + str(is_detecting_eyes)

    if is_detecting_eyes:
        telemetry += ', EAR: ' + str(EAR)

    cv2.putText(img, telemetry,
                text_loc, font,
                1, (255, 255, 255), 2)

    # show frame
    cv2.imshow('Asthenopia Assistant', img)

    return [EAR, timestamp, is_detecting_eyes]
# end face_analysis()

def face_analysis_calibration():
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    EAR = -1
    # set up telemetry
    timestamp = str(dt.datetime.now())[11:]
    is_detecting_eyes = False
    # face analysis
    faces = detector(gray)
    for face in faces:
        # 36 - 47 are the landmarks for the eyes
        landmarks = predictor(gray, face)

        # compute EAR from left eye (reference: png file)
        upper_eye = (
            int((landmarks.part(37).x + landmarks.part(38).x) / 2),
            int((landmarks.part(37).y + landmarks.part(38).y) / 2))
        lower_eye = (
            int((landmarks.part(40).x + landmarks.part(41).x) / 2),
            int((landmarks.part(40).y + landmarks.part(41).y) / 2))
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(39).x, landmarks.part(39).y)
        # ratio of distances

        vert_len = math.sqrt(math.pow(upper_eye[0] - lower_eye[0], 2) + math.pow(upper_eye[1] - lower_eye[1], 2))
        horiz_len = math.sqrt(math.pow(left_eye[0] - right_eye[0], 2) + math.pow(left_eye[1] - right_eye[1], 2))
        EAR = round(vert_len / horiz_len, 2)

        # on screen eye telemetry
        cv2.line(img, upper_eye, lower_eye, (255, 0, 0), 2)
        cv2.line(img, left_eye, right_eye, (255, 0, 0), 2)
        for n in range(36, 48):
            is_detecting_eyes = True
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            # dot each landmark
            cv2.circle(img, (x, y), 4, (255, 255, 255), -1)

    # generate and display telemetry
    telemetry = 'Calibrating... ' \
                + ' eyes detecting: ' \
                + str(is_detecting_eyes)

    if is_detecting_eyes:
        telemetry += ', EAR: ' + str(EAR)

    cv2.putText(img, telemetry,
                text_loc, font,
                1, (255, 255, 255), 2)

    # show frame
    cv2.imshow('Asthenopia Assistant', img)

    return [EAR, timestamp, is_detecting_eyes]


# start program
print('starting calibration...')
calibration_time = 50

ear_threshold_calc = []
while len(ear_threshold_calc) < calibration_time:
    ear_threshold_calc.append(face_analysis_calibration())
    if cv2.waitKey(1) == 27:
        break

avg = 0
ear_min = 1
ear_max = 0
for i in range(calibration_time):
    if ear_threshold_calc[i][0] > 0:
        avg += ear_threshold_calc[i][0]
    if ear_threshold_calc[i][0] > ear_max:
        ear_max = ear_threshold_calc[i][0]
    if ear_threshold_calc[i][0] < ear_min:
        ear_min = ear_threshold_calc[i][0]

avg /= 50
ear_threshold = ear_min + 0.2 * (ear_max - ear_min)
EAR_data[1] = ear_threshold

print('Finished calibration with threshold: ' + str(ear_threshold))


EAR_data[0] = dt.datetime.now().strftime('%m/%d/%Y %H:%M')
# loop for EAR detection
while True:
    EAR_data.append(face_analysis())

    # slice last byte and check if key pressed is esc
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

for i in EAR_data:
    print(i)
