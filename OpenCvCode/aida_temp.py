# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

coordinates = [[[55, 750], [3708.5]], [[643, 747], [3326.0]], [[545, 746], [3373.0]], [[448, 746], 
                [3421.5]], [[350, 746], [3476.0]], [[253, 747], [3592.0]], [[55, 650], [3768.0]], 
                [[642, 648], [3455.5]], [[447, 648], [3498.0]], [[350, 648], [3517.5]], [[253, 648], 
                 [3594.0]], [[642, 549], [3537.0]], [[155, 550], [3748.0]], [[641, 451], [3560.5]], 
                 [[544, 451], [3600.0]], [[447, 451], [3610.0]], [[155, 451], [3794.5]], [[253, 352], 
                  [3738.5]], [[155, 352], [3852.0]], [[155, 253], [3967.5]], [[56, 251], [4021.0]]]
print('here are coords', len(coordinates))

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

    new_lst = [list(x) for x in zip(row_no, col_no)]
    print(new_lst)
    return  col_no, row_no, new_lst
#Felix wants most recently played disk column
points = get_x_and_y_coord_from_contours(coordinates)
x_, y_ , merged = get_row_and_col(points)

def find_top_and_bottom_coord_of_each_col(col_no, row_no, new_lst, points):
    col_1 = []
    col_2 = []
    col_3 = []
    col_4 = []
    col_5 = []
    col_6 = []
    
    for i in range(len(row_no)):
        print(i)
        
        if new_lst[i][1] == 1 and new_lst[i][0] == 1:
            col_1.append(points[i])
            print('found top disk of column 1', new_lst[i], points[i])
            
        if new_lst[i][1] == 1 and new_lst[i][0] == 6:
            col_1.append(points[i])
            print('found bottom disk of column 1', new_lst[i], points[i])
                
        if new_lst[i][1] == 2 and new_lst[i][0] == 1:
            col_2.append(points[i])
            print('found top disk of column 2', new_lst[i], points[i])       
            
        if new_lst[i][1] == 2 and new_lst[i][0] == 6:
            col_2.append(points[i])
            print('found bottom disk of column 2', new_lst[i], points[i])

        if new_lst[i][1] == 3 and new_lst[i][0] == 1:
            col_3.append(points[i])
            print('found top disk of column 3', new_lst[i], points[i])
       
        if new_lst[i][1] == 3 and new_lst[i][0] == 6:
            col_3.append(points[i])
            print('found bottom disk of column 3', new_lst[i], points[i])     
        
        if new_lst[i][1] == 4 and new_lst[i][0] == 1:
            col_4.append(points[i])
            print('found top disk of column 4', new_lst[i], points[i])
        
        if new_lst[i][1] == 4 and new_lst[i][0] == 6:
            col_4.append(points[i])
            print('found bottom disk of column 4', new_lst[i], points[i])
            
        if new_lst[i][1] == 5 and new_lst[i][0] == 1:
            col_5.append(points[i])
            print('found top disk of column 5', new_lst[i], points[i])
        
        if new_lst[i][1] == 5 and new_lst[i][0] == 6:
            col_5.append(points[i])
            print('found bottom disk of column 5', new_lst[i], points[i])

        if new_lst[i][1] == 6 and new_lst[i][0] == 1:
            col_6.append(points[i])
            print('found top disk of column 6', new_lst[i], points[i])
        
        if new_lst[i][1] == 5 and new_lst[i][0] == 6:
            col_6.append(points[i])
            print('found bottom disk of column 6', new_lst[i], points[i])
        
    print('FINISHED BLUE COORDS', 'col 1:', col_1, 'col 2:',col_2, 'col 3:',col_3, 'col 4:', col_4, 'col 5:',col_5, 'col 6:',col_6)
            
            
find_top_and_bottom_coord_of_each_col(x_, y_ , merged, points)