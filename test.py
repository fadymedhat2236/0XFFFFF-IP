import requests
import json
class OCRSpaceLanguage:
    Arabic = 'ara'
    English = 'eng'

class OCRSpace:
    def __init__(self, api_key, language=OCRSpaceLanguage.English):
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


API_KEY = 'e9925d2b1f88957'

ocr = OCRSpace(API_KEY,OCRSpaceLanguage.Arabic)
results = ocr.ocr_file('./card.jpg')
lines_arr = results['ParsedResults'][0]['TextOverlay']['Lines']

for i in range(len(lines_arr)):
    words_arr = lines_arr[i]['Words']
    for j in range(len(words_arr)):
        print words_arr[j]
        print words_arr[j]['WordText'].encode('utf-8')
