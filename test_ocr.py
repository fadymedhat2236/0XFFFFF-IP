from test import OCRSpace,OCRSpaceLanguage
import base64
from io import BytesIO
from PIL import Image
import cv2


im = cv2.imread('card_out.jpg')
pil_img = Image.fromarray(im)
buff = BytesIO()
pil_img.save(buff, format="JPEG")
new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")

API_KEY = 'e9925d2b1f88957'
results = OCRSpace(API_KEY,new_image_string,OCRSpaceLanguage.Arabic).get_lines()

print results