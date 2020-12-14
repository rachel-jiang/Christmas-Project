# Documentation

3 to 5 years old kids will need early childhood development toys. This toy is made for the kids making connection between color and words.



First, importing all the packages that we need

```python
import cv2 #opencv for color detection and image processing
import numpy as np #for making array, help color detection
import random #random pick the color for user to find
import RPi.GPIO as GPIO #lighting
from time import sleep #for the camera warming up, motor turning time and light on time
from picamera import PiCamera #for the camera, photo taking
```

set the breadboard

```python
GPIO.setmode(GPIO.BOARD)
```

Make the color range. 

Here is the sample range, you can make a trackbar to adjust.

In the following code, it includes **red, blue and green**.

```python
# Red color range
lower_red = np.array([161, 155, 84])
upper_red = np.array([179, 255, 255])

# Green
lower_green = np.array([25, 52, 72])
upper_green = np.array([90, 255, 255])

# Blue
lower_blue = np.array([90, 52, 150])
upper_blue = np.array([100, 255, 255])
```

Next we need to set the camera.

make sure you put make a function for this, otherwise it will give an error called "out of resource" when you ran the second time.

```python
camera = PiCamera()


def Take_an_Image():
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(5)
    camera.capture("foo.jpg")
```



Now we have our basic information, we can start a while loop.

Also, we need to set two initial value here.

```python
while True:
    var="none"
    bu="false"
    user = "y"
```

random choose a color(red/green/blue) from the list and print it for the user.

```python
color = ["red", "green", "blue"]
x = (random.choice(color))
print("find" + " " + x)
```

Now the user will choose one of the card, pick the matching one and click the button to take a photo of it. 

The following code is for detecting if the button clicked.

```python
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
if GPIO.input(32) == GPIO.HIGH:
    bu = "true"
else:
    bu="false"
```

*if the button pressed, then bu=true, if it is not, it stay false.*

Now adding another if statement when bu equals to true

```python
if bu=="true":
```

<u>make sure to spell right</u>

if the button pressed, then take a photo of the card. Call the function.

```python
Take_an_Image()
```

Read the image and **convert the image from "BGR" into "HSV" mode**.

```python
img = cv2.imread('foo.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

**HSV stands for "hue, saturation, lightness", BGR stands for "blue green red"*

Once you have the HSV image, we can start the color detection and see if it matches the color printed before. 

The process is following:

1. Making a mask for the image
2. Adding pixels for each column
3. Finding the max value of the column
4. If it is great then 150000, then yes, the user picked the right one
5. Otherwise, the user picked wrong

```python
if x=="red":
    mask = cv2.inRange(hsv, lower_red, upper_red)#make the image black and white
    histValues = np.sum(mask, axis=0)#adding pixels of each column(either 255 or 0 for each pixel)
    maxValue = np.max(histValues)#find the max value
    if maxValue >= 150000:#if the value is greater than 150000
        var = "yes"
    else:
        var = "no"
elif x=="green":
    mask = cv2.inRange(hsv, lower_green, upper_green)
    histValues = np.sum(mask, axis=0)
    maxValue = np.max(histValues)
    if maxValue >= 150000:
        var = "yes"
    else:
        var = "no"
elif x=="blue":
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    histValues = np.sum(mask, axis=0)
    maxValue = np.max(histValues)
    if maxValue >= 150000:
        var = "yes"
    else:
        var = "no"
else:
    pass
```

*The var value will tell you if the user picked the right one. If it is right, var=yes, if it is incorrect, var=no*

You can also print the var, image and mask for testing.

```python
#print(var)
#print(maxValue)
#cv2.imshow('image', img)#show original image
#cv2.imshow('mask', mask)#show mask in black and white

#cv2.waitKey(0)
#cv2.destroyAllWindows()
```

Then we need to make another if statement

When the user picked the right one, the doll on the top will start dancing in circle. Also, it will ask the user if they want to play it again or they wanna quit.

```python
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
```

***it is important adding the else, because the user may not see the "(y/n)", so they may enter other stuff and there will be an error.**

When the user choose the wrong color (var equals to false), red light is going to on, and it's going to tell the user that he is wrong. 

It will ask if the user want to keep going or not.

```python
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
```

Finally, this will break the whole while loop

```python
if user == "y":
    pass
elif user == "n":
    break
else:
    pass
```

