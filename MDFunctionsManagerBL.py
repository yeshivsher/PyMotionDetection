import os
import MDRedis
from datetime import datetime

NUM_OF_ARGUMENTS_INPUT = 10


# Check if arguments are exists and valid.
def checkArgsValidation(argv):
    print(argv)
    if(len(argv) != NUM_OF_ARGUMENTS_INPUT + 1): # including the file name.
        print('\nInput Error: {} parameters were not accepted.'.format(NUM_OF_ARGUMENTS_INPUT))
        print("""Required: camera-address object-size-detection-min object-size-detection-max frequency-detection sensitivity number-of-frames-to-skip GuidId CameraId CameraName CamerAlertFileName.""")
            
        return False
    return True

# Display the output JSON.
def printAllData(movementsList):
    print('\n\n' 
        + '#########################################' 
        + '\nPrinting all data:'
        + '#########################################') 

    for l in movementsList:
        tempMovementsList = movementsList[l]

        print('\n')
        print('Frame ID: ' + str(l))
        print('Time: ' + str(tempMovementsList['Time']))
        # print('Image Name: ' + str(tempMovementsList['Image Name']))
        print('Movements in this frame:')

        tempMovements = tempMovementsList['Movements']

        for m in tempMovements:
            tempMovement = tempMovements[m]

            print('\t\t' + 'Movement: ' + str(m))
            print('\t\t' + 'Location: ' + str(tempMovement['Location']))
            print('\t\t' + 'Size: ' + str(tempMovement['Size']))

    print('\n\n')

# Create the dir to keep the images.
def createImagesDir():
    if not os.path.exists('movements images'):
        os.makedirs('movements images')


def preperVideoDataQStringToRedis(GuidId, CameraId, CameraName, CamerAlertFileName, PositionDetectedList):
    value = """{{"GuidId":"{}","CameraId":{},"CameraName":"{}","CamerAlertFileName":"{}","IsMotionDetectionMsg":true,"PositionDetectedList":{},"AzimuthDeg":45.0,"PhotoTime":"{}","UpdateTime":"{}","IsCameraConneted":true}}""".format(GuidId, CameraId, CameraName, CamerAlertFileName, PositionDetectedList, datetime.now(), datetime.now())
    
    return value
    
    # 2019-08-05T20:08:22.2574777+03:00