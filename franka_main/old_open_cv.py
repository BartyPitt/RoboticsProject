# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:19:24 2020

@author: aidam
"""

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
            #print(area)
            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #print(area)
                output.append([[cX ,cY],[area]])
                #print(output)
                #print('cX:', cX, 'cY:', cY)
            except ZeroDivisionError:
                pass
    return output

#def plot_centre_line(row, column):
#    for i in row:
#        point1 = 

def get_x_and_y_coord_from_contours(coordinates):   
    counter = -1
    coords = []
    for i in coordinates:
        counter += 1
        y_coord = coordinates[counter][0][1]
        x_coord = coordinates[counter][0][0]
        coords.append([x_coord, y_coord])       
    return coords
    
def get_row_and_col(coordinates):
    counter = -1
    x = []
    y = []
    col_no = []
    row_no = []
    for i in coordinates:  
        counter += 1
        #print(counter)
        y_coord = coordinates[counter][1]
        y.append(y_coord)
        x_coord = coordinates[counter][0]
        #print(x_coord)
        x.append(x_coord)
    for x_coord in x:
        
        if 50 < x_coord < 60:
            col = 1
        elif 150 < x_coord < 160:
            col = 2   
        elif 245 < x_coord < 260:
            col = 3   
        elif 330 < x_coord < 360:
            col = 4
        elif 440 < x_coord < 460:
            col = 5
        elif 540 < x_coord < 550:
            col = 6
        elif 630 < x_coord < 650:
            col = 7
        col_no.append(col)
    
    for y_coord in y:
        #print(y_coord ,'test')
        if 250 < y_coord < 260:
            row = 1
        elif 340 < y_coord < 360:
            row = 2
        elif 440 < y_coord < 460:
            row = 3
        elif 540 < y_coord < 560:
            row = 4
        elif 640 < y_coord < 660:
            row = 5
        elif 740 < y_coord < 760:
            row = 6
        row_no.append(row)

    result = [list(x) for x in zip(row_no, col_no)]
    #print(result)
    return result

#Felix wants most recently played disk column
    
def TransformTheImage(img,Extension):  
    '''Takes the image and transforms it , extension if you want to see above the grid.  ''' 
    #Red Contours
    lower_red = np.array([0,110,139])
    upper_red = np.array([10,255,255])
    
    RedContours = ConvectionFunction(img,lower_red , upper_red)
    Red_cordinates = ContourInfo(RedContours , 500)
    
    Squared = [x[0][0] * x[0][1] for x in Red_cordinates]
    #for x in Red_cordinates:
        #print( "test", x[0][1])
    
    Red_cordinates = [x[0] for _, x in sorted(zip(Squared,Red_cordinates), key=lambda pair: pair[0])] # like a cheaky zip for when the going gets rough.
    
    pts_dst = np.array([[0,Extension] , [0,600 + Extension] , [700,Extension] ,[700 , 600 + Extension]],np.float32)
    Red_cordinates = np.array(Red_cordinates,np.float32)

    #h, status = cv2.findHomography(pts_src, Red_cordinates)
    #h = cv2.getPerspectiveTransform(Red_cordinates,pts_dst)
    h, _ = cv2.findHomography(Red_cordinates,pts_dst)
    SquareImage = cv2.warpPerspective(img, h,(700,600 + Extension))
    ImageInlineShow(SquareImage)

    return SquareImage



def GetPositions(ImageLocation):
    '''Takes In an Image Location and returns what the current layout of the parts is'''

    img = cv2.imread(ImageLocation)
    SquareImage = TransformTheImage(img,200)
    #If the Extra space at the top starts causing problems. 

    #The Blue ask
    lower_blue = np.array([90,130,80])
    upper_blue = np.array([115,255,255])
    
    blueContours = ConvectionFunction(SquareImage,lower_blue , upper_blue)
    blue_cordinates = ContourInfo(blueContours , 500)
    blue_points = get_x_and_y_coord_from_contours(blue_cordinates)
    blue_cols_and_rows = get_row_and_col(blue_points)   
    print('BLUE COLS AND ROWS', blue_cols_and_rows)

    #The Yellow Mask
    lower_yellow = np.array([20,204,150])
    upper_yellow = np.array([54,255,255])
    
    yellowContours = ConvectionFunction(SquareImage,lower_yellow, upper_yellow)
    yellow_cordinates = ContourInfo(yellowContours , 500)
    yellow_points = get_x_and_y_coord_from_contours(yellow_cordinates)
    yellow_cols_and_rows = get_row_and_col(yellow_points)
    print('YELLOW COLS AND ROWS', yellow_cols_and_rows)

#GetPositions('Grid1.jpg')
