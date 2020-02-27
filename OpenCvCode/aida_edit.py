# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:19:24 2020

@author: aidam
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt



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
        y_coord = coordinates[counter][1]
        y.append(y_coord)
        x_coord = coordinates[counter][0]
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

    new_lst = [list(x) for x in zip(row_no, col_no)]
    #print(new_lst)
    return  col_no, row_no, new_lst

def find_top_and_bottom_coord_of_each_col(col_no, row_no, new_lst, points):
    '''Function that finds the top and bottom disk coordinates of each column. 
      Returns an array for each column with the coordinate of the  top and bottom disk'''
    col_1 = []
    col_2 = []
    col_3 = []
    col_4 = []
    col_5 = []
    col_6 = []
    
    for i in range(len(row_no)):
        #print(i)
        
        if new_lst[i][1] == 1 and new_lst[i][0] == 1:
            col_1.append(points[i])
            #print('found top disk of column 1', new_lst[i], points[i])
            
        if new_lst[i][1] == 1 and new_lst[i][0] == 6:
            col_1.append(points[i])
            #print('found bottom disk of column 1', new_lst[i], points[i])
    
        if new_lst[i][1] == 2 and new_lst[i][0] == 1:
            col_2.append(points[i])
 
        if new_lst[i][1] == 2 and new_lst[i][0] == 6:
            col_2.append(points[i])

        if new_lst[i][1] == 3 and new_lst[i][0] == 1:
            col_3.append(points[i])

        if new_lst[i][1] == 3 and new_lst[i][0] == 6:
            col_3.append(points[i])   
        
        if new_lst[i][1] == 4 and new_lst[i][0] == 1:
            col_4.append(points[i])
        
        if new_lst[i][1] == 4 and new_lst[i][0] == 6:
            col_4.append(points[i])

        if new_lst[i][1] == 5 and new_lst[i][0] == 1:
            col_5.append(points[i])

        if new_lst[i][1] == 5 and new_lst[i][0] == 6:
            col_5.append(points[i])
 
        if new_lst[i][1] == 6 and new_lst[i][0] == 1:
            col_6.append(points[i])

        if new_lst[i][1] == 5 and new_lst[i][0] == 6:
            col_6.append(points[i])
    #print('FINISHED COORDS', 'col 1:', col_1, 'col 2:',col_2, 'col 3:',col_3, 'col 4:', col_4, 'col 5:',col_5, 'col 6:',col_6)    
    return col_1, col_2, col_3, col_4, col_5, col_6
    

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

def plot_centre_line(column, ImageLocation): 
    '''Takes in target column and latest captured image and finds centreline of column'''
    #The aim is would be to have a red dot on the centre of the gripper, get coords from that point.
    #Then you can calculate by how many columns off is the gripper if it has not gone to the correct position
    point_1 = tuple(column[0])
    point_2 = tuple(column[1])
    color = (0,0,255)
    img = cv2.imread(ImageLocation)
    #ImageInlineShow(img)
    img = cv2.imread(ImageLocation,cv2.IMREAD_COLOR)
    cv2.line(img, point_1,point_2,color,5)
    cv2.imshow('image',img)
    cv2.waitKey(0)

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
                output.append([[cX ,cY],[area]])
            except ZeroDivisionError:
                pass
    return output

def list_connector(list1, list2):
    '''Function to merge lists of coordinates. Used to join yellow and blue disk coords'''
    output = list1+list2
    return output
            
def TransformTheImage(img,Extension):  
    '''Takes the image and transforms it , extension if you want to see above the grid.  ''' 
    #Red Contours
    lower_red = np.array([0,110,139])
    upper_red = np.array([10,255,255])
    
    RedContours = ConvectionFunction(img,lower_red , upper_red)
    Red_cordinates = ContourInfo(RedContours , 500)
    
    Squared = [x[0][0] * x[0][1] for x in Red_cordinates]
    
    Red_cordinates = [x[0] for _, x in sorted(zip(Squared,Red_cordinates), key=lambda pair: pair[0])] # like a cheaky zip for when the going gets rough.
    
    pts_dst = np.array([[0,Extension] , [0,600 + Extension] , [700,Extension] ,[700 , 600 + Extension]],np.float32)
    Red_cordinates = np.array(Red_cordinates,np.float32)

    h, _ = cv2.findHomography(Red_cordinates,pts_dst)
    SquareImage = cv2.warpPerspective(img, h,(700,600 + Extension))
    ImageInlineShow(SquareImage)

    return SquareImage

def GetPossitions(ImageLocation):
    '''Takes In an Image Location and returns what the current layout of the parts is'''
   

    img = cv2.imread(ImageLocation)
    SquareImage = TransformTheImage(img,200)
    #If the Extra space at the top starts causing problems. 

    #The Blue mask
    lower_blue = np.array([90,130,80])
    upper_blue = np.array([115,255,255])
    
    blueContours = ConvectionFunction(SquareImage,lower_blue , upper_blue)
    blue_coordinates = ContourInfo(blueContours , 500)

    #The Yellow Mask
    lower_yellow = np.array([20,204,150])
    upper_yellow = np.array([54,255,255])
    
    yellowContours = ConvectionFunction(SquareImage,lower_yellow, upper_yellow)
    yellow_coordinates = ContourInfo(yellowContours , 500)
    

#--------------------------------------------------------------------------------------------------------#
    #Joining the contour info output of the yellow and the blue disks
    coordinates = list_connector(blue_coordinates, yellow_coordinates) 
    #removing the area and keeping only the x and y centre coordinates
    points = get_x_and_y_coord_from_contours(coordinates)
    #converting pixles to rows list (x_), columns list(y_), and merging to list of coordinates in terms of
    #row and columns. Eg: [55, 750] is now [6, 1]
    x_, y_ , merged = get_row_and_col(points)
    #function to find top and bottom position of disks in each column.
    column1, column2, column3, column4, column5, column6 = find_top_and_bottom_coord_of_each_col(x_, y_ , merged, points)
    plot_centre_line(column1, ImageLocation) #Here it should take whichever column the robot is placing
                                                #the next disk on, and the lastest image the webcam took
    
GetPossitions('/Users/aidam/Desktop/Robotics Coursework/Images/WithRedDot/Grid1.jpg')

# =============================================================================
# TO DO:
# ROSNODE PUBLISHER AND SUBSCRIBER
# OUTPUT PROCESSED IMAGES
# FINISH LINE DRAWING FUNCTION
# CALL LINE DRAWING ON PROCESSED IMAGE
# 
# FUNCTION TO CONVERT DISKS POSITIONS TO ARRAY OF 1S AND -1S - DONE
# SNAPSHOT CODE TO TAKE IMAGE1 AND IMAGE2 AT AN INTERVAL
# SUBTRACT BOARDS - DONE
# IF DIFFERENCE = 0 RETURN NO DISK PLACED
# ELSE, FIND AND RETURN COORD OF NEW DISK PLACED - DONE
# 
# FROM FELIX CODE:
# IF OUTPUT IS THAT ROBOT HAS PLAYED AND NO NEW DISK DETECTED:
# CALL LAST MOTION PLAN AGAIN
# IF ROBOT HAS PLAYED AND NEW DISK DETECTED:
# FIND ROBOT COORD, DETECTED COORD. 
# SUBTRACT THEM FROM EACH OTHER
# IF NOT 0
# SET ROBOT COORD TO DETCTED COORD
# CONTINUE GAME FROM THIS COORD
# =============================================================================