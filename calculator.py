import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import button as bt

# Webcam
cap = cv.VideoCapture(0)

cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# We want to detect only ONE hand
detector = HandDetector(detectionCon=0.5, maxHands=1)

# BUTTON
display = (255, 255, 255)
numbers = (237, 250, 170)
operations = (170, 227, 250)
submit = (185, 148, 247)

# Creating Buttons
buttonValues = [["7", "8", "9", "*"],
                ["4", "5", "6", "-"],
                ["1", "2", "3", "+"],
                ["0", "/", ".", "="]]

buttonList = []
for x in range(4):
    for y in range(4):

        xpos = x*100 + 800
        ypos = y*100 + 150

        color = ()
        if(x < 3 and y < 3):
            color = numbers
        if (x == 3 or y == 3):
            color = operations
        if (x == 3 and y == 3):
            color = submit
        if (x == 0 and y == 3):
            color = numbers

        buttonList.append(
            bt.Button(position=(xpos, ypos), width=100, height=100, text=buttonValues[y][x], color=color))


# VARIABLES

# to store the whole equation from the calculator
equation = ""
# for avaoiding duplicates
delayCounter = 0

# LOOPING

while True:
    # Get image from webcam
    success, image = cap.read()

    # Flip the image horizontally
    image = cv.flip(src=image, flipCode=1)

    # Detect hand
    # Used mediapipe package in the backend
    # As we have already flipped the image we dont want findHands to flip it
    hands, image = detector.findHands(img=image, flipType=False)

    # DRAW BUTTONS

    # Display screen
    cv.rectangle(img=image, pt1=(800, 50), pt2=(800+400, 70+100),
                 color=display, thickness=cv.FILLED)
    cv.rectangle(img=image, pt1=(800, 50), pt2=(
        800+400, 70+100), color=(0, 0, 0), thickness=3)

    for button in buttonList:
        button.draw(image)

    # Check Hand
    if hands:
        lmList = hands[0]["lmList"]  # Has all the points on hand

        # print(lmList[8][:2])
        # print("ok")

        # We are interested in index tip(8) and middle tip(12)
        distance, _, image = detector.findDistance(
            lmList[8][:2], lmList[12][:2], image)

        x, y = lmList[8][:2]

        if(distance < 50):
            for i, button in enumerate(buttonList):
                if button.clicked(image, x, y) and delayCounter == 0:
                    val = buttonValues[i % 4][i//4]

                    if val == "=":
                        equation = str(eval(equation))
                    else:
                        equation += val

                    delayCounter = 1

    # Avoid Duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Display Equation/Result
    cv.putText(img=image, text=equation, org=(810, 110),
               fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=3, color=(0, 0, 0), thickness=3)

    # Display image
    cv.imshow("Screen", image)

    # 1 second delay
    key = cv.waitKey(1)

    if(key == ord("c")):  # to clear the display calculator
        equation = ""

    if(key == ord('q')):  # to stop the program
        break
