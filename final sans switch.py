 import cv2
import numpy as np
import pyautogui
import time
import random as rd

precision = 20
# set the window size and position of the Minecraft game
win_width = int(1920)
win_height = int(1080)
win_x = int(50)
win_y = int(50)

# set the coordinates of the region of interest (ROI) containing the slider
roi_x = int(350)
roi_y = int(520)
roi_width = int(1100)
roi_height = int(50)

# set the color thresholds for red, orange, and violet
red_thresh = [0, 100, 100]
red_max = [10, 255, 255]
orange_thresh = [10, 100, 150]
orange_max = [30, 255, 255]
violet_thresh = [120, 100, 150]
violet_max = [140, 255, 255]

# set the coordinates of the space bar
space_x = 650*2
space_y = 900*2

# set the refresh rate of the screen capture (in milliseconds)
refresh_rate = 10
weel_time =  time.time()

while True:
    timeun = rd.randint(1, 5)
    timedn = rd.randint(1, 59)

    # Sleep for a random time
    time.sleep(timeun + timedn / 60.0)
    start_time = time.time()
    timeout = 60  # secondes

    a=5
    pyautogui.click(button='right')




    # loop until the user presses the 'q' key
    while a>1:
        if time.time() - start_time > timeout:
            print("La boucle a été arrêtée après 30 secondes.")
            a=0
        if time.time() - weel_time > 60:
            print("on change de canne")
            # pyautogui.scroll(-10)
            weel_time =  time.time()


        # capture the screenshot of the Minecraft game window
        screenshot = pyautogui.screenshot(region=(win_x, win_y, win_width, win_height))

        # convert the screenshot to a numpy array and BGR format
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # extract the ROI containing the slider
        roi = screenshot[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width, :]

        # convert the ROI to HSV color space
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # create masks for the red, orange, and violet sections of the slider
        red_mask = cv2.inRange(hsv, np.array(red_thresh), np.array(red_max))
        orange_mask = cv2.inRange( hsv, np.array(orange_thresh), np.array(orange_max))
        violet_mask = cv2.inRange(hsv, np.array(violet_thresh), np.array(violet_max))

        # create a white mask by thresholding the grayscale image
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, white_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

        # pad the white mask to make it 2 pixels larger than the real size of the slider
        white_mask = cv2.copyMakeBorder(white_mask, 1, 1, 0, 0, cv2.BORDER_CONSTANT, value=0)

        # find the position of the slider by finding the center of mass of the white pixels
        moments = cv2.moments(white_mask, False)
        if moments["m00"] != 0.0:
            slider_x = int(moments["m10"] / moments["m00"])
            slider_y = int(moments["m01"] / moments["m00"])

            # check if there is any orange present in the ROI
            if np.any(orange_mask):

                # find the center of the orange section by finding the center of mass of the orange pixels
                moments_orange = cv2.moments(orange_mask, False)
                if moments_orange["m00"] != 0.0:
                    orange_x = int(moments_orange["m10"] / moments_orange["m00"])
                    orange_y = int(moments_orange["m01"] / moments_orange["m00"])

                    # check if the slider is in the orange section of the bar
                    if abs(slider_x - orange_x) < precision:
                        # simulate the space bar press
                        pyautogui.press('space')
                        print('orange')
                        print("Space bar pressed")
                        time.sleep(0.1)
                        start_time = time.time()
                        a=0

            # check if there is any violet present in the ROI
            elif np.any(violet_mask):
                # find the center of the violet section by finding the center of mass of the violet pixels
                moments_violet = cv2.moments(violet_mask, False)
                if moments_violet["m00"] != 0.0:
                    violet_x = int(moments_violet["m10"] / moments_violet["m00"])
                    violet_y = int(moments_violet["m01"] / moments_violet["m00"])

                    # check if the slider is in the violet section of the bar
                    if abs(slider_x - violet_x) < precision:
                        # simulate the space bar press
                        pyautogui.press('space')
                        print('violet')
                        print("Space bar pressed")
                        time.sleep(0.1)
                        start_time = time.time()
                        a=0

            # check if there is any red present in the ROI
            elif np.any(red_mask):
                # find the center of the red section by finding the center of mass of the red pixels
                moments_red = cv2.moments(red_mask, False)
                if moments_red["m00"] != 0.0:
                    red_x = int(moments_red["m10"] / moments_red["m00"])
                    red_y = int(moments_red["m01"] / moments_red["m00"])

                    # check if the slider is in the red section of the bar
                    if abs(slider_x - red_x) < precision:
                        # simulate the space bar press
                        pyautogui.press('space')
                        print('red')
                        print("Space bar pressed")
                        time.sleep(0.1)
                        start_time = time.time()
                        a=0


        # display the red, orange, violet, and white masks
        #cv2.imshow('Red Mask', red_mask)
        #cv2.imshow('Orange Mask', orange_mask)
        #cv2.imshow('Violet Mask', violet_mask)
        cv2.imshow('White Mask', white_mask)

        # wait for a key press to close the windows
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # wait for the next refresh cycle
        time.sleep(refresh_rate / 1000.0)

    # close all open windows
    cv2.destroyAllWindows()