import cv2
import time
import handtrackingmodule as htm
import numpy as np
import os
import mediapipe as mp

overlayList = []  # list to store all the images

brushThickness = 25
eraserThickness = 100
drawColor = (255, 0, 255)  # setting purple color

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # defining canvas

# images in header folder
folderPath = "Header"  # assuming the Header folder is in the same directory as the script
currentDir = os.path.dirname(__file__)  # get the current directory
folderPath = os.path.join(currentDir, folderPath)  # join the current directory with the folder path

if os.path.exists(folderPath):  # check if the folder exists
    myList = os.listdir(folderPath)  # getting all the images used in code
    # print(myList)
    for imPath in myList:  # reading all the images from the folder
        image = cv2.imread(os.path.join(folderPath, imPath))
        overlayList.append(image)  # inserting images one by one in the overlayList
    header = overlayList[0]  # storing 1st image
else:
    print("Header folder not found. Please create a Header folder in the same directory as the script.")
    exit()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                if draw:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
        return bbox

    def fingersUp(self):
        fingers = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            if myHand.landmark[4].y < myHand.landmark[3].y:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if myHand.landmark[4 * id + 3].y < myHand.landmark[4 * id + 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

detector = htm.handDetector(detectionCon=1, maxHands=1)  # making object

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)  # for neglecting mirror inversion

    # 2. Find Hand Landmarks
    img = detector.findHands(img)  # using functions fo connecting landmarks
    lmList, bbox = detector.findPosition(img,
                                         draw=False)  # using function to find specific landmark position,draw false means no circles on landmarks

    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]  # tip of index finger
        x2, y2 = lmList[12][1], lmList[12][2]  # tip of middle finger

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. If selection mode - Two finger are up!
        if fingers[1] == 1 and fingers[2] == 1:
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If drawing mode - Index finger is up!
        if fingers[1] == 1 and fingers[2] == 0:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()