# -*- coding: utf-8 -*-
import numpy as np
import cv2
import imutils
from ocr_pkg.ocr import OCRSpace,OCRSpaceLanguage
import base64
from io import BytesIO
from PIL import Image

#PARAMETERS
GAUSSIAN_KERNEL_SIZE = 5
CANNY_MIN_THRESH = 75
CANNY_MAX_THRESH = 200
DILATION_KERNEL_SIZE = 5
EPSILON_TORELANCE = 0.02
ADATIVE_SIZE = 11
ADAPTIVE_C = 10

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
	"""
	cv2.imshow("step1",edges)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	#contour and get the largest 5 contours
	cnts = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

	#find the card contour
	found = False
	for c in cnts:
		epsilon =  EPSILON_TORELANCE*cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c,epsilon, True)
		if len(approx) == 4:
			card = approx
			found = True
			break
	if found == False:
		return False
	cv2.drawContours(image, [card], -1, (0, 255, 0), 2)
	"""
	cv2.imshow("step2", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	cropped = four_point_transform(original, card.reshape(4, 2))
	cropped_gray = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
	words = cv2.adaptiveThreshold(cropped_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,ADATIVE_SIZE,ADAPTIVE_C)
	
	"""
	cv2.imshow("step3",words)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	#return the card image only
	#cv2.imwrite('image.jpg',words)
	return True,words

# functions for dealing with the ocr response
def leftCompare(element):
	return element[2]
def all_arabic_numbers(element): 
	arabic_numbers_array= [u'\u0660',u'\u0661',u'\u0662',u'\u0663',u'\u0664',u'\u0665',u'\u0666',u'\u0667',u'\u0668',u'\u0669']
	length = len(element)
	if length == 0:
		return False
	for i in range(length):
		if element[i] not in arabic_numbers_array:
			return False
	return True
def to_english(id):
	translate = {u'\u0660':0,u'\u0661':1,u'\u0662':2,u'\u0663':3,u'\u0664':4,u'\u0665':5,u'\u0666':6,u'\u0667':7,u'\u0668':8,u'\u0669':9}
	en_id=""
	for x in id:
		if x in translate:
			en_id+=str(translate[x])
	return en_id

def get_lines(image,sort=True):
	# turn numpy array image into a base64 encoded string
	#get portion of image
	kernel = np.ones((3,3),np.uint8)
	if sort:
		im = image[int(image.shape[0]*2.9/4):int(image.shape[0]*3.7/4),int(image.shape[1]*1.2/3):]
		im = cv2.pyrUp(im)
		im = cv2.morphologyEx(255-im, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
		#cv2.imwrite('N_num.jpg',im)
	else:
		im = image[int(image.shape[0]*0.4):int(image.shape[0]*0.8),:int(image.shape[1]*0.8)]
		im = cv2.pyrUp(im)
		im = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
		#cv2.imwrite('F_num.jpg',im)
	"""
	cv2.imshow('portion',im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	pil_img = Image.fromarray(im)
	buff = BytesIO()
	pil_img.save(buff, format="JPEG")
	new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
	# call ocr api
	API_KEY = 'e9925d2b1f88957'
	results = OCRSpace(API_KEY,new_image_string,OCRSpaceLanguage.Arabic).get_lines()
	# re-arrange the lines
	length = results[len(results)-1][0] + 1
	lines = []
	for i in range(length):
		line = [n for n in results if n[0]==i]
		if sort:
			line = sorted(line,key=leftCompare) 
			lines.append(''.join([x[1] for x in line]))
		else:
			#to keep the space that splits the name 
			lines.append(' '.join([x[1] for x in line]))
	return lines
	
	
def get_national_id(lines):
	for i in range(len(lines)):
		#print lines[i]
		if all_arabic_numbers(lines[i]):
			return lines[i]
def get_faculty_id_name(lines):
	# assume length of name > 12 and start search from above
	name = ""
	name_index = 0
	for i in range(len(lines)):
		if((len(lines[i])) > 8) and (lines[i][len(lines[i])-1].isnumeric()==False):
			name=lines[i]
			name_index = i
			break
	#print(lines[name_index],"   " ,name_index)
	#print lines
	
	faculty_id = ""
	# search for 7 digits in the line beneath the name
	for j in range(name_index+1,len(lines)):
		for i in range(0,len(lines[j])):
			#print lines[j][i]
			if lines[j][i].isnumeric():
				faculty_id = lines[j][i:i+7]
				break
	#print faculty_id
	return faculty_id,name

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
def analyze_image(studentIdImage, nationalIdImage):
	ret = get_card(studentIdImage)
	if ret[0]==False:
		return 'please take another photo of your faculty card'
	student_card = ret[1]
	ret = get_card(nationalIdImage)
	if ret[0]==False:
		return 'please take another photo of your national card'
	national_card = ret[1]
	#n = get_lines(national_card)
	im = national_card[int(national_card.shape[0]*3.1/4):int(national_card.shape[0]*3.6/4),int(national_card.shape[1]*1.2/3):]
	#im = cv2.pyrUp(im)
	im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
	"""
	cv2.imshow("img",im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	n_id=str(pytesseract.image_to_string(im,lang='ara_number',config =tessdata_dir_config)).replace(" ","")
	f = get_lines(student_card,False)
	#n_id =  get_lines(national_card)[0]
	f_id,name =  get_faculty_id_name(f)
	print(n_id)
	print(f_id)
	return True,name,f_id,n_id
	
