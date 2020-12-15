import cv2
import numpy as np
import random
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

GPIO.setmode(GPIO.BOARD)
# Red color range
lower_red = np.array([161, 155, 84])
upper_red = np.array([179, 255, 255])

# Green
lower_green = np.array([25, 52, 72])
upper_green = np.array([90, 255, 255])

# Blue
lower_blue = np.array([90, 52, 150])
upper_blue = np.array([100, 255, 255])

camera = PiCamera()


def Take_an_Image():
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(5)
    camera.capture("foo.jpg")


while True:
    var = "none"
    bu = "false"
    user = "y"

    color = ["red", "green", "blue"]
    x = (random.choice(color))
    print("find" + " " + x)

    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if GPIO.input(32) == GPIO.HIGH:
        bu = "true"
    else:
        bu = "false"

    while bu == "true":

        """camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture('foo.jpg')"""

        Take_an_Image()

        img = cv2.imread('foo.jpg')

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        if x == "red":
            mask = cv2.inRange(hsv, lower_red, upper_red)
            histValues = np.sum(mask, axis=0)
            maxValue = np.max(histValues)
            print(maxValue)
            if maxValue >= 150000:
                var = "yes"
            else:
                var = "no"
        elif x == "green":
            mask = cv2.inRange(hsv, lower_green, upper_green)
            histValues = np.sum(mask, axis=0)
            maxValue = np.max(histValues)
            print(maxValue)
            if maxValue >= 150000:
                var = "yes"
            else:
                var = "no"
        elif x == "blue":
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            histValues = np.sum(mask, axis=0)
            maxValue = np.max(histValues)
            print(maxValue)
            if maxValue >= 110000:
                var = "yes"
            else:
                var = "no"
        else:
            var = "no"

        #print(var)

        if var == "yes":
            GPIO.setup(16, GPIO.OUT)
            GPIO.output(16, GPIO.HIGH)
            sleep(5)
            GPIO.output(16, GPIO.LOW)
            user = raw_input("This is" + " " + x + ",you are awesome! Do you want to keep playing(y/n)?")
            if user == "y":
                bu == "false"
                break
            elif user == "n":
                print("Bye! Good job today and see you next time!")
                sleep(2)
                bu == "false"
                break
            else:
                print("I am assuming you want to quit. Good job today and see you next time!")
                sleep(2)
                user = "n"
                bu == "false"
                break

        if var == "no":
            # light up
            GPIO.setup(12, GPIO.OUT)
            GPIO.output(12, GPIO.HIGH)
            sleep(5)
            GPIO.output(12, GPIO.LOW)
            user = raw_input("This is not" + " " + x + ", do you want to keep playing(y/n)?")
            if user == "y":
                bu == "false"
                break
            elif user == "n":
                print("Bye! Good job today and see you next time!")
                sleep(2)
                bu == "false"
                break
            else:
                print("I am assuming you want to quit.")
                sleep(2)
                user == "n"
                bu == "false"
                break
        else:
            pass
    if user == "y":
        pass
    elif user == "n":
        break
    else:
        pass

    # cv2.imshow('image', img)
    # cv2.imshow('mask', mask)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
