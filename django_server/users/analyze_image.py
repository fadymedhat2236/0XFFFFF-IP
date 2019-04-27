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
ADATIVE_SIZE = 11
ADAPTIVE_C = 7

def order_points(pts):
	# return is array of pts ordered as top_left,top_right,bottom_right,bottom_left
	rect = np.zeros((4, 2), dtype = "float32")
	
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	return rect

def four_point_transform(image, pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	perfect_rect = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	# prespective transform
	M = cv2.getPerspectiveTransform(rect, perfect_rect)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	return warped


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
		if len(shape) == 4:
			card = shape
			break
	cv2.drawContours(image, [card], -1, (0, 255, 0), 2)
	
	cropped = four_point_transform(original, card.reshape(4, 2))
	cropped_gray = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
	words = cv2.adaptiveThreshold(cropped_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,ADATIVE_SIZE,ADAPTIVE_C)
	
	
	return words
	
	
def analyze_image(studentIdImage, nationalIdImage):
	student_card = get_card(studentIdImage)
	national_card = get_card(nationalIdImage)
	return 'name','faculty_id','national_id'
