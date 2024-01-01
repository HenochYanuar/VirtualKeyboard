import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0) # Get the input video from default camera
# Setting resolution input to 1280 x 720
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8) # Used class HandDetector whit detection confidence value is 0.8

# Declaration array which stored character on keyboard
keys = \
    [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["SPACE"]
    ]

finalText = "" # Variable to store any character pressed

def drawAll(image, listButton): # Function for create/draw keyboard objects on the screen

    for btn in listButton: # Get the every instance from buttonList variable
        coordinateX, coordinateY = btn.pos # Get the X-coordinate and Y-coordinate points of each button
        width, height = btn.size # Get the width and height of each button
        cvzone.cornerRect(image, (btn.pos[0], btn.pos[1], btn.size[0], btn.size[1])) # Create/draw bounding box on each edge of the button
        cv2.rectangle(image, btn.pos, (coordinateX + width, coordinateY + height), (255, 0, 255), cv2.FILLED) # Make the shape of the button according to the position, X and Y coordinates, as well as the width and height of each button size
        cv2.putText(image, btn.text, (coordinateX + 8, coordinateY + 30), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 255, 255), 2) # Place each text/character into each button that has been created

    return image # Return from drawAll Function

class Button: # Create a Button class to declare the attributes of each button
    def __init__(self, pos, text, size=None):
        self.text = text # Set the button text according to the text parameter
        if size is None: # If the size from parameter is None
            if self.text == "SPACE": # If the button text is "SPACE"
                size = [205, 40] # Set the size of button
            else: # If the button text is not "SPACE"
                size = [40, 40] # Set the size of button

        self.pos = pos # Set the button position according to the pos parameter
        self.size = size # Set the button size according to the size parameter

buttonList = [] # The variable to store each key added from the Button class corresponds to the value of the keys variable

keyboard = Controller() # Used to control the keyboard by typing text

for i in range(len(keys)): # Keys variable looping
    for j, key in enumerate(keys[i]): # Looping each iteration on a key variable
        buttonList.append(Button([55 * j + 20, 55 * i + 20], key)) # Set the position and key(text) of button using Button class and append to buttonList[]

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img) # Detected there a hand on the input
    img = drawAll(img, buttonList) # Call the drawAll function to draw every value from buttonList[] like keyboard objects on the screen
    if hands: # If a hand is detected
        hand1 = hands[0] # Get the data from detected hand
        lmList1 = hand1["lmList"] # Get the landmarks from detected hand
        x8, y8, _ = lmList1[8] # Get the x and y coordinates of the landmark point 8 (tip of index finger) on the hand
        x12, y12, _ = lmList1[12] # Get the x and y coordinates of the landmark point 12 (tip of the middle finger) on the hand
        for button in buttonList: # # Get the every instance from buttonList variable
            x, y = button.pos # Get the X-coordinate and Y-coordinate points of each button
            w, h = button.size # Get the width and height of each button

            if x< lmList1[8][0]<x+w and y< lmList1[8][1]<y+h: # If the coordinates of landmarks point 8 (tip of index finger) are at one of the coordinates of the button
                cvzone.cornerRect(img, (button.pos[0] - 5, button.pos[1] - 5, button.size[0] + 10, button.size[1] + 10), colorC=(255, 0, 255)) # Create/draw bounding box on each edge of the button
                cv2.rectangle(img, (x-5, y-5), (x + w + 5, y + h + 5), (0, 225, 0), cv2.FILLED) # Change the shape and color of the button according to the X and Y coordinates, as well as the width and height of each button size
                cv2.putText(img, button.text, (x + 8, y + 30), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 255, 255), 2) # Place each text/character into each button that has been created

                length, info, img = detector.findDistance((x8, y8), (x12, y12), img) # Find the length of the distance between the tip of the index finger to the tip of the middle finger

                # Click / Press a button
                if length<30: # If the length of the distance between the tip of the index finger to the tip of the middle finger is less then 30
                    if button.text == "SPACE": # If the button text is "SPACE"
                        keyboard.press(' ') # Print a space on the screen
                    else: # If the button text is not "SPACE"
                        keyboard.press(button.text) # Print the text/character of the button

                    cvzone.cornerRect(img, (button.pos[0] - 5, button.pos[1] - 5, button.size[0] + 10, button.size[1] + 10), colorC=(255, 0, 255)) # This line is equal to the 71 th line
                    cv2.rectangle(img, (x-5, y-5), (x + w + 5, y + h + 5), (95, 95, 95), cv2.FILLED)# This line is equal to the 72 th line
                    cv2.putText(img, button.text, (x + 8, y + 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 255, 255), 2) # This line is equal to the 73 - 74th line

                    if button.text == "SPACE": # If the button text is "SPACE"
                        finalText += ' ' # Append the empty string to finalText variable
                    else:  # If the button text is not "SPACE"
                        finalText += button.text # Append the button text to finalText variable
                    sleep(0.25) # Each time you click, the program can't click again for 0.25 seconds

    # Make a rectangle as a place to put the pressed button character
    cv2.rectangle(img, (50, 350), (700, 450), (0, 225, 0), cv2.FILLED) # Create the rectangle
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 255, 255), 3) # Put the every value from finalText

    cv2.imshow("image", img)
    cv2.waitKey(1)
