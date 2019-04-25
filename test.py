import requests
import json
import cv2
import base64
from io import BytesIO
from PIL import Image

class OCRSpaceLanguage:
    Arabic = 'ara'
    English = 'eng'

class OCRSpace:
    def __init__(self, api_key,string_file, language=OCRSpaceLanguage.English):
        """ ocr.space API wrapper
        :param api_key: API key string
        :param language: document language
        """
        self.api_key = api_key
        self.language = language
        self.payload = {
            'isOverlayRequired': True,
            'apikey': self.api_key,
            'language': self.language,
            'base64Image':'data:image/jpeg;base64,'+string_file,
        }

    def ocr_file(self, filename):
        """ OCR.space API request with local file
        :param filename: Your file path & name
        :return: Result in JSON format
        """
        with open(filename, 'rb') as f:
            r = requests.post(
                'https://api.ocr.space/parse/image',
                files={filename: f},
                data=self.payload,
            )
        return r.json()

    def ocr_string(self):
        """ OCR.space API request with local file
        :param filename: Your file path & name
        :return: Result in JSON format
        """
        
        r = requests.post(
                'https://api.ocr.space/parse/image',
                data=self.payload
            )
        return r.json()


API_KEY = 'e9925d2b1f88957'


im = cv2.imread('card_out.jpg')
pil_img = Image.fromarray(im)
buff = BytesIO()
pil_img.save(buff, format="JPEG")
new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
#results = ocr.ocr_file('./card_out.jpg')
ocr = OCRSpace(API_KEY,new_image_string,OCRSpaceLanguage.Arabic)
results = ocr.ocr_string()
lines_arr = results['ParsedResults'][0]['TextOverlay']['Lines']
#words and locations array --> word , top , left
words_locations =[]
for i in range(len(lines_arr)):
    words_arr = lines_arr[i]['Words']
    for j in range(len(words_arr)):
        current = words_arr[j] 
        print words_arr[j]
        print words_arr[j]['WordText'].encode('utf-8')
        words_locations.append([current['WordText'].encode('utf-8'),current['Top'],current['Left']])
print words_locations
