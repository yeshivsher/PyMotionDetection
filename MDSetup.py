import numpy as np
import cv2
import time
import uuid
from datetime import datetime
import MDFunctionsManagerBL
import MDFunctionsManagerDAL
import sys

if(not MDFunctionsManagerBL.checkArgsValidation(sys.argv)):
    sys.exit()

## Opencv consts.
CAMERA_ADDRESS = sys.argv[1] == '0' if int(sys.argv[1]) else 0  # 0 to default cammera.
OBJECT_SIZE_DETECTION_MIN = int(sys.argv[2]) # 3000
OBJECT_SIZE_DETECTION_MAX = int(sys.argv[3]) # 63000
FREQUENCY_DETECTION = int(sys.argv[4]) # 2
SENSITIVITY = int(sys.argv[5]) # 20
NUM_OF_FRAMES_TO_SKIP = int(sys.argv[6]) # 5
## Redis consts.
GUID_ID = sys.argv[7]
CAMERA_ID = int(sys.argv[8])
CAMERA_NAME = sys.argv[9]
CAMER_ALERT_FILE_NAME = sys.argv[10]

# init objects.
video_capture = cv2.VideoCapture(CAMERA_ADDRESS)

ret, frame1 = video_capture.read()
ret, frame2 = video_capture.read()

# init vars.
start = int(time.time())
movment_location = (0, 0)
isSecondFrame = False 
movementsList = {}
movementsData = {}
frameData = {}
latestFrame = None
movementsNumPerFrame = 0
frameCounter = 0
numOfFramesToSkip = 0

PositionDetected = {}
PositionDetectedList = []

while(video_capture.isOpened()):
    # Init the params.
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, SENSITIVITY, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2)
    # cv2.contourArea(contour) # the real size. 

    # There is movment int this frame.
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        recSize = h * w

        # Checking the size of the object.
        if recSize < OBJECT_SIZE_DETECTION_MIN:
            continue

        # In case we need to ignore some events.
        if numOfFramesToSkip > 0:
            numOfFramesToSkip = numOfFramesToSkip - 1
            continue

        # In case there is a light or unecpected event, skeeping X frames.
        if recSize > OBJECT_SIZE_DETECTION_MAX:
            numOfFramesToSkip = NUM_OF_FRAMES_TO_SKIP
            continue

        if isSecondFrame:
            # Send location every X seconds.
            if (int(start + FREQUENCY_DETECTION) > int(time.time())):
                continue

        movementsNumPerFrame = movementsNumPerFrame + 1

        # Taking the middle of the movement.
        # movment_location = (x + int(w/2), y + int(h/2))
        movment_location2 = (x + int(w/2), int(h))
        
        PositionDetected['Lat'] = x + int(w/2)
        PositionDetected['Lng'] = y + int(h/2)
        PositionDetected['Alt'] = 0.0
        
        PositionDetectedList.append(PositionDetected)

        tempMovementData = {}
        tempMovementData['Location'] = movment_location
        tempMovementData['Size'] = str(recSize)

        movementsData[movementsNumPerFrame] = tempMovementData

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 5)

        # add some extra info to the frame.
        # cv2.putText(frame1, "Movement", (15, 25),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        #movment_location = (x + int(w/2), y + int(h/2))
        #frame1 = cv2.circle(frame1, movment_location, 40, (0, 255, 0), 5)
        frame1 = cv2.circle(frame1, movment_location, 5, (0, 0, 255), 5)

    # Request with movement.
    # Do after each frame.
    if len(movementsData) > 0:
        print('required movements:')
        print(len(movementsData))
        print('movements:')
        print(len(contours))
        
        
        VideoDataQStringToRedis = MDFunctionsManagerBL.preperVideoDataQStringToRedis(GUID_ID, CAMERA_ID, CAMERA_NAME, CAMER_ALERT_FILE_NAME, 
            PositionDetectedList)
        MDFunctionsManagerDAL.sendVideoDataQToRedis(CAMERA_NAME, VideoDataQStringToRedis)

        start = int(time.time())
        isSecondFrame = True
        movementsNumPerFrame = 0
        frameCounter = frameCounter + 1

        # Save the movement data.
        now = datetime.now()

        frameData['Time'] = now.strftime("%d/%m/%Y %H:%M:%S")
        frameData['Movements'] = movementsData

        movementsList[uuid.uuid4().hex] = frameData

        latestFrame = list(movementsList.keys())[-1]

        movementsData = {}
        frameData = {}
        PositionDetectedList = []
        

    elif (int(start + FREQUENCY_DETECTION) <= int(time.time())):
        print('There is no movement.')
        start = int(time.time())
        isSecondFrame = False
        uncommonCasesFlag = False

    # Display each frame.
    cv2.imshow("Motion detection", frame1)
    frame1 = frame2
    ret, frame2 = video_capture.read()

    # Exit.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# MDFunctionsManagerBL.printAllData(movementsList)

# Release the camera
video_capture.release()
cv2.destroyAllWindows()

print("Bye...")

