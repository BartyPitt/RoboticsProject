"""
Created on Mon Feb  3 22:19:24 2020

@author: aidam
@author: Barty Pitt
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

def ImageInlineShow(Image):
    Run = True
    '''
    A function to show the images in line instead of as sperate images designed for Jupyter Notepad.'''
    if Run:
        plt.imshow(cv2.cvtColor(Image, cv2.COLOR_BGR2RGB))
        plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        plt.show()

def get_x_and_y_coord_from_contours(coordinates):
    '''Takes in information about the contours in the form of [[cX ,cY],[area]], and keeps
    [cX, cY], which are the pixel coordinates of the centre of each disk.'''
    counter = -1
    coords = []
    for i in coordinates:
        counter += 1
        y_coord = coordinates[counter][0][1]
        x_coord = coordinates[counter][0][0]
        coords.append([x_coord, y_coord])
    return coords

def get_row_and_col(coordinates):
    '''Takes pixel coordinates in the form of [cX ,cY], and returns the row for cX, and column for cY'''
    Tolerance = 20 #a tolerance is added to check the coordinate in the row/column are within a range.
    xList = []
    yList = []
    KeyX = [55 , 155 , 250 , 345 , 450 , 545 , 640] #these are the estimated pixels in which the coordinates for each column lie in
    KeyY = [200 , 330 , 430 , 530 , 650 , 760] #these are the estimated pixels in which the coordinates for each row lie in
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
    return col_1, col_2, col_3, col_4, col_5, col_6


def disks_to_array(board):
    '''Function takes in the positions of all the disks on the board and returns a numpy
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
    Takes in an Image,
    the lower bounds and the upper bounds
    and returns the contours for the image and the thresholds, as well as the processed image.
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

def plot_centre_line(column_list, img):
    '''Function that takes a list of the top and bottom coordinates of each column, and an image,
    and plots a centreline down the given column'''
    point_1 = tuple(column_list[0]) #convert to tuple as opencv function only takes in tuple
    point_2 = tuple(column_list[1])
    color = (0,0,255)
    cv2.line(img, point_1,point_2,color,5)
    cv2.imshow('image',img)
    cv2.waitKey(0)

def ContourInfo(contours ,minArea):
    '''Takes in a set of contours returns the cordinate for the centre of the the ones above a certain size'''
    output = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > minArea:
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
    '''Takes the image and transforms it, the extension is added to see above the grid.  '''
    #Red Contours
    lower_red1 = np.array([0,110,39])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([159,39,139])
    upper_red2 = np.array([179,255,255])


    RedContours, __ = ConvectionFunction(img,[lower_red1,lower_red2], [upper_red1,upper_red2])
    Red_cordinates = ContourInfo(RedContours , 100)
    Red_cordinates = [x[0] for x in Red_cordinates]
    if len(Red_cordinates) != 4:
        print("cant locate red dots")
    else:
        Red_cordinates = CordinatesSorter(Red_cordinates)


    pts_dst = np.array([[700 , 600 + Extension], [0,600 + Extension],[700,Extension] ,[0,Extension] ] ,np.float32)
    Red_cordinates = np.array(Red_cordinates,np.float32)
    h, _ = cv2.findHomography(Red_cordinates,pts_dst)
    SquareImage = cv2.warpPerspective(img, h,(700,600 + Extension))
    ImageInlineShow(SquareImage)

    return SquareImage

def ArrayfromCordinates(Cordinates1 , Cordinates2 = None):
    '''Takes in one or two sets of cordninates , and returns a combined array.'''
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

    '''It reads an image from the given Image Location, flattens it, finds the yellow and the blue disks,
        and returns the rows and columns of each of the disks.'''
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

def SnapShotAndPossition():
    '''Takes an image with the webcam and then puts it through the position finding algorithm.'''
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
