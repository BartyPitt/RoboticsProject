# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:19:24 2020

@author: aidam
@author: Barty Pitt
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

def ImageInlineShow(Image):
    Run = True
    '''
    A function to show the images in line instead of as sperate images designed for Jupyter Notepad.
    Sabotage me if you dont want anything being printed out
    In simple terms it stops the kernal from stopping when it wants to print an image.
    '''
    if Run:
        plt.imshow(cv2.cvtColor(Image, cv2.COLOR_BGR2RGB))
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()

def get_x_and_y_coord_from_contours(coordinates):
    '''Takes in a 3 by x matricie and removes the first column'''
    counter = -1
    coords = []
    for i in coordinates:
        counter += 1
        y_coord = coordinates[counter][0][1]
        x_coord = coordinates[counter][0][0]
        coords.append([x_coord, y_coord])       
    return coords

def get_row_and_col(coordinates):
    '''Takes Pixel Cordinates and returns row and collumn'''
    Tolerance = 20
    xList = []
    yList = []
    KeyX = [55 , 155 , 250 , 345 , 450 , 545 , 640]
    KeyY = [200 , 330 , 430 , 530 , 650 , 760]
    for i in coordinates:        
        y_coord = i[1]
        x_coord = i[0]
        for n,x in enumerate(KeyX):
            if abs(x_coord - x) < Tolerance:
                xList.append(n)
                break
        else:
            print("x out" , x_coord)
            pass
        for n,y in enumerate(KeyY):
            if abs(y_coord - y) < Tolerance:
                yList.append(n)
                break
        else:
            xList.pop(-1)
            print("Y out" , y_coord)
    return [cord for cord in zip(xList , yList)]

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
        
        if new_lst[i][1] == 0 and new_lst[i][0] == 0:
            col_1.append(points[i])
            print('found top disk of column 1', new_lst[i], points[i])
            
        if new_lst[i][1] == 0 and new_lst[i][0] == 5:
            col_1.append(points[i])
            #print('found bottom disk of column 1', new_lst[i], points[i])
    
        if new_lst[i][1] == 1 and new_lst[i][0] == 0:
            col_2.append(points[i])
 
        if new_lst[i][1] == 1 and new_lst[i][0] == 5:
            col_2.append(points[i])

        if new_lst[i][1] == 2 and new_lst[i][0] == 0:
            col_3.append(points[i])

        if new_lst[i][1] == 2 and new_lst[i][0] == 5:
            col_3.append(points[i])   
        
        if new_lst[i][1] == 3 and new_lst[i][0] == 0:
            col_4.append(points[i])
        
        if new_lst[i][1] == 3 and new_lst[i][0] == 5:
            col_4.append(points[i])

        if new_lst[i][1] == 4 and new_lst[i][0] == 0:
            col_5.append(points[i])

        if new_lst[i][1] == 4 and new_lst[i][0] == 5:
            col_5.append(points[i])
 
        if new_lst[i][1] == 5 and new_lst[i][0] == 0:
            col_6.append(points[i])

        if new_lst[i][1] == 5 and new_lst[i][0] == 5:
            col_6.append(points[i])
    print('FINISHED COORDS', 'col 1:', col_1, 'col 2:',col_2, 'col 3:',col_3, 'col 4:', col_4, 'col 5:',col_5, 'col 6:',col_6)    
    return col_1, col_2, col_3, col_4, col_5, col_6
    

def disks_to_array(board):
    '''this function takes in the positions of all the disks on the board and returns a numpy
    array with -1 for the bot disks and 1 for the player disks'''
        
    for x in np.nditer(board, op_flags=['readwrite']):
        if x[...] == 1:
            x[...] = -1
        if x[...] == 2:
            x[...] = 1
    return board

def where_is_the_new_disk(board1, board2):
    '''this function takes in the board state before the human plays (board1) and after they play
    (board2), and subtracts them from each other. Where the result is not 0 it returns the column 
    and row of that position, which is where the new disk has been played'''
    board_before = disks_to_array(board1)
    board_after = disks_to_array(board2)
    result = np.subtract(board_before, board_after)
    for x in np.nditer(result):
        if x[...] != 0:
            i, j = np.where(result != 0)
    return i, j #i is row, j is col

def ConvectionFunction(Image ,LowerBounds , UpperBounds):
    '''
    Takes in an Image , 
    the lower bounds and the upper bounds 
    and returns the contours for the image and the thresholds
    '''

    hsv = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV) # Convert to hsv
    for LowerMask,UpperMask in zip(LowerBounds,UpperBounds):
        LowerBound = np.array(LowerMask) # Remove if ALL of the code inputs a numpy array into the function
        UpperBound = np.array(UpperMask)
        mask = cv2.inRange(hsv , LowerBound,UpperBound) # Creates the mask
        try: 
            outputMask = outputMask | mask
        except NameError:
            outputMask = mask
    kernel = np.ones((5,5),np.uint8)
    outputMask = cv2.morphologyEx(outputMask,cv2.MORPH_OPEN,kernel)
    ImageInlineShow(outputMask)

    contours , _ = cv2.findContours(outputMask , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE) # Creates contours from the mask
    print("Length of contours is " ,len(contours))
    img2 = Image.copy()
    index = -1
    thickness = 10
    colour = (255 , 0 , 255)
    
    cv2.drawContours(img2,contours , index , colour , thickness)

    ImageInlineShow(img2)
    return contours, img2

def plot_centre_line(column, img): 
    '''THIS FUNCTION IS NOT CURRENTLY WORKING BECAUSE THE IMAGE THAT IT NEEDS TO TAKE IN TO DRAW THE LINE
    IS NOT BEING OUTPUTTED/SAVED ANYWHERE YET. CURRENTLY WORKING ON FIXING THAT'''
    point_1 = tuple(column[0])
    print(point_1)
    point_2 = tuple(column[1])
    print(point_1)
    color = (0,0,255)
    cv2.line(img, point_1,point_2,color,5)
    cv2.imshow('image',img)
    cv2.waitKey(0)

def ContourInfo(contours ,minArea):
    
    '''
    Takes in a set of contours returns the cordinate for the centre of the the ones above a certain size
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

def CordinatesSorter(Cordinates):
    '''Takes in the cordinates and orders by the first two varibles'''
    CordinatesWithIndex = sorted(zip([i for i in range(4)] , Cordinates, [0 for i in range(4)]) , key=lambda Cordinate: Cordinate[1][0])
    CordinatesWithIndex = list(CordinatesWithIndex)
    for i in range(2):
        CordinatesWithIndex[i] = list(CordinatesWithIndex[i])
        CordinatesWithIndex[i][2] += 1
    CordinatesWithIndex.sort(key=lambda Cordinate: Cordinate[1][1])
    for i in range(2):
        CordinatesWithIndex[i] = list(CordinatesWithIndex[i])
        CordinatesWithIndex[i][2] += 2
    CordinatesWithIndex.sort(key=lambda Cordinate: Cordinate[2])
    output = [x[1] for x in CordinatesWithIndex]
    return output

       
def TransformTheImage(img,Extension):  
    '''Takes the image and transforms it , extension if you want to see above the grid.  ''' 
    #Red Contours
    lower_red1 = np.array([0,110,39])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([159,39,139])
    upper_red2 = np.array([179,255,255])

    
    RedContours, __ = ConvectionFunction(img,[lower_red1,lower_red2], [upper_red1,upper_red2])
    Red_cordinates = ContourInfo(RedContours , 100)
    #print("Pre removed" , Red_cordinates)
    Red_cordinates = [x[0] for x in Red_cordinates]
    if len(Red_cordinates) != 4:
        print("cant locate red dots")
    else:
        Red_cordinates = CordinatesSorter(Red_cordinates)


    pts_dst = np.array([[700 , 600 + Extension], [0,600 + Extension],[700,Extension] ,[0,Extension] ] ,np.float32)
    #print(Red_cordinates)
    Red_cordinates = np.array(Red_cordinates,np.float32)
    h, _ = cv2.findHomography(Red_cordinates,pts_dst)
    SquareImage = cv2.warpPerspective(img, h,(700,600 + Extension))
    ImageInlineShow(SquareImage)

    return SquareImage

def ArrayfromCordinates(Cordinates1 , Cordinates2 = None):
    '''
    Takes in one or two sets of cordninates , and returns a combined array.
    '''
    output = np.zeros((7,6))
    for co in Cordinates1:
        y,x = co
        output[y][x] = 1
    if Cordinates2 == None:
        return output    
    for co in Cordinates2:
        y,x = co
        output[y][x] = 2
    return output
        


def GetPossitions(img ,Location = True):
         
    '''Takes In an Image Location and returns what the current layout of the parts is'''
    if Location:
         img = cv2.imread(img)

    SquareImage = TransformTheImage(img,200)
    #If the Extra space at the top starts causing problems. 

    #The Blue mask
    lower_blue = np.array([90,130,80])
    upper_blue = np.array([115,255,255])
    
    blueContours, __ = ConvectionFunction(SquareImage,[lower_blue] , [upper_blue])
    blue_coordinates = ContourInfo(blueContours , 800)

    #The Yellow Mask
    lower_yellow = np.array([20,55,70])
    upper_yellow = np.array([45,191,200])
    
    yellowContours, __ = ConvectionFunction(SquareImage,[lower_yellow], [upper_yellow])
    yellow_coordinates = ContourInfo(yellowContours , 800)
    
    mergedy = get_row_and_col(get_x_and_y_coord_from_contours(yellow_coordinates))
    mergedb = get_row_and_col(get_x_and_y_coord_from_contours(blue_coordinates))
    Board = ArrayfromCordinates(mergedb,mergedy)
    return disks_to_array(Board)
    
    camera.release()
    
    

def SnapShotAndPossition():
    '''Takes an image with the webcam and then puts it through the possiton finding algorythm.'''
    camera = cv2.VideoCapture(0)
    for i in range(10):
        __, frame = camera.read()
    frame = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
    ImageInlineShow(frame)
    Board = GetPossitions(frame , Location = False)
    camera.release()
    return Board


if __name__ == "__main__":
    '''Functional Test Code'''
    board2 = np.zeros((7,6))
    while True:
        board1 = (SnapShotAndPossition())
        print(board1)
        i , j = where_is_the_new_disk(board1,board2)
        print("the col is", j)
        k = input()
        if k == "q":
            break
        board2 = board1




    #GetPossitions('/Users/aidam/Desktop/Robotics Coursework /Images/WithRedDot/Grid1.jpg')


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