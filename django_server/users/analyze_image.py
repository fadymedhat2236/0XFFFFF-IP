# -*- coding: utf-8 -*-
import numpy as np
import cv2
import imutils

#PARAMETERS
GAUSSIAN_KERNEL_SIZE = 5
CANNY_MIN_THRESH = 75
CANNY_MAX_THRESH = 200
DILATION_KERNEL_SIZE = 5
EPSILON_TORELANCE = 0.02

def get_card(image):
	original = image.copy()
	#find edges and dilation
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray_blured = cv2.GaussianBlur(gray, (GAUSSIAN_KERNEL_SIZE,GAUSSIAN_KERNEL_SIZE), 0)
	edges = cv2.Canny(gray_blured, CANNY_MIN_THRESH, CANNY_MAX_THRESH)
	kernel = np.ones((DILATION_KERNEL_SIZE,DILATION_KERNEL_SIZE),np.uint8)
	edges = cv2.dilate(edges,kernel)
	
	#contour and get the largest 5 contours
	cnts = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

	#find the card contour
	for c in cnts:
		epsilon =  EPSILON_TORELANCE*cv2.arcLength(c, True)
		shape = cv2.approxPolyDP(c,epsilon, True)
		if len(approx) == 4:
			card = shape
			break
	cv2.drawContours(image, [card], -1, (0, 255, 0), 2)
	
	
def analyze_image(studentIdImage, nationalIdImage):
	student_card = get_card(studentIdImage)
	national_card = get_card(nationalIdImage)
	return 'name','faculty_id','national_id'
