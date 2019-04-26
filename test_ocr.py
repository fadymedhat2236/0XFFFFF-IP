from test import OCRSpace,OCRSpaceLanguage
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

im = cv2.imread('Ncard1_out.jpg')
pil_img = Image.fromarray(im)
buff = BytesIO()
pil_img.save(buff, format="JPEG")
new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")

API_KEY = 'e9925d2b1f88957'
results = OCRSpace(API_KEY,new_image_string,OCRSpaceLanguage.Arabic).get_lines()
#print 'results :',results
length = results[len(results)-1][0] + 1
"""
for i in range(length):
	for j in range(len(results)):
		if results[j][0]==i:
			print results[j][1].encode('utf-8'),"   ",results[j][2],' : ',i
"""
lines = []
def leftCompare(element):
	return element[2]
for i in range(length):
	line = [n for n in results if n[0]==i]
	from_left_to_right = sorted(line,key=leftCompare) 
	lines.append(''.join([x[1] for x in from_left_to_right]))
	#print line
	#print 'lines',lines
#print 'lines',lines

# 0->9 u'\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669'

def all_arabic_numbers(element):
	arabic_numbers_array= [u'\u0660',u'\u0661',u'\u0662',u'\u0663',u'\u0664',u'\u0665',u'\u0666',u'\u0667',u'\u0668',u'\u0669']
	length = len(element)
	for i in range(length):
		
		if element[i] not in arabic_numbers_array:
			return False
	return True

for i in range(len(lines)):
	
	if all_arabic_numbers(lines[i]):
		print lines[i].encode('utf-8')
		break