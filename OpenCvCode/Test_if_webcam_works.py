# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:39:14 2020

@author: aidam
"""
import numpy as np
import cv2


cap = cv2.VideoCapture(1)
# Check if the webcam is opened correctly
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret,frame = cap.read()

    cv2.imshow('Original video',frame)

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()