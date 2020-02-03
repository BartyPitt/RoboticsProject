''' 
A set of functions designed to detect connect 4 boards with open cv

If you need help please dont email me.

Made by :
    ____             __       
   / __ )____ ______/ /___  __
  / __  / __ `/ ___/ __/ / / /
 / /_/ / /_/ / /  / /_/ /_/ / 
/_____/\__,_/_/   \__/\__, /  
    ____  _ __  __   /____/   
   / __ \(_) /_/ /_           
  / /_/ / / __/ __/           
 / ____/ / /_/ /_             
/_/   /_/\__/\__/         

Aiiiiiiida
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt



def ImageInlineShow(Image):
    '''
    A function to show the images in line instead of as sperate images designed for Jupyter Notepad.
    Sabotage me if you dont want anything being printed out.
    '''
    plt.imshow(cv2.cvtColor(Image, cv2.COLOR_BGR2RGB))
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


def ConvectionFunction(Image ,LowerBound , UpperBound):
    '''
    Takes in an Image , the lower bounds and the upper bounds and returns the contours for the image and the thresholds
    TODO add in Adaptive thresholding if needed
    '''
    hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV) # Convert to hsv
    
    LowerBound = np.array(LowerBound) # Remove if ALL of the code inputs a numpy array into the function
    UpperBound = np.array(UpperBound)
    
    mask = cv2.inRange(hsv , LowerBound , UpperBound) # Creates the mask
    contours , _ = cv2.findContours(mask , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE) # Creates contours from the mask
    
    img2 = Image.copy()
    index = -1
    thickness = 10
    colour = (255 , 0 , 255)
    
    cv2.drawContours(img2,contours , index , colour , thickness)

    ImageInlineShow(img2)
    return contours


def ContourInfo(contours ,minArea):
    '''
    Takes in a set of contours returns the cordinate for the centre of the the ones above a certain size
    TODO ADD TEST FOR IF IT IS A CIRCLE RATHER THAN JUST doing it by overal area
     '''
    output = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > minArea:
            print(area)
            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print(area)
                output.append([[cX ,cY],[area]])
            except ZeroDivisionError:
                pass
    return output


def GetPossitions(ImageLocation):
    '''Takes In an Image Location and returns what the current layout of the parts is'''
    img = cv2.imread(ImageLocation)
    
    #Red Contours
    lower_red = np.array([0,110,139])
    upper_red = np.array([10,255,255])
    
    RedContours = ConvectionFunction(img,lower_red , upper_red)
    Red_cordinates = ContourInfo(RedContours , 500)
    
    Squared = [x[0][0] * x[0][1] for x in Red_cordinates]
    
    Red_cordinates = [x[0] for _, x in sorted(zip(Squared,Red_cordinates), key=lambda pair: pair[0])] # like a cheaky zip for when the going gets rough.
    print(Red_cordinates)
    
    pts_dst = np.array([[0,0] , [0,600] , [700,0] ,[700 , 600]],np.float32)
    Red_cordinates = np.array(Red_cordinates,np.float32)

    #h, status = cv2.findHomography(pts_src, Red_cordinates)
    h = cv2.getPerspectiveTransform(Red_cordinates,pts_dst)
    SquareImage = cv2.warpPerspective(img, h,(700,600))

    ImageInlineShow(SquareImage)
    
    #The Blue mask
    lower_blue = np.array([90,130,80])
    upper_blue = np.array([115,255,255])
    
    blueContours = ConvectionFunction(SquareImage,lower_blue , upper_blue)
    blue_cordinates = ContourInfo(blueContours , 500)
    print("Blue Cordinates")
    print(blue_cordinates)

    #The Yellow Mask
    lower_yellow = np.array([20,204,150])
    upper_yellow = np.array([54,255,255])
    
    yellowContours = ConvectionFunction(SquareImage,lower_yellow, upper_yellow)
    yellow_cordinates = ContourInfo(yellowContours , 500)
    
    #End of barty Code I am unsure what you want me to return aida.



GetPossitions('Refference Images/WithRedDot/Grid1.jpg')