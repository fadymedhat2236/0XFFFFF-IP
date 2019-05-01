import requests
import json

class OCRSpaceLanguage:
    Arabic = 'ara'
    English = 'eng'

class OCRSpace:
    def __init__(self, api_key,string_file, language=OCRSpaceLanguage.English):
       
        self.api_key = api_key
        self.language = language
        self.payload = {
            'isOverlayRequired': True,
            'apikey': self.api_key,
            'language': self.language,
            'base64Image':'data:image/jpeg;base64,'+string_file,
        }

    def ocr_string(self):
        
        r = requests.post(
                'https://api.ocr.space/parse/image',
                data=self.payload
            )
        return r.json()


    def get_lines(self):
        """
        return the array of lines --> index of the line and the contents of the line
        """
        results = self.ocr_string()
        lines_arr = results['ParsedResults'][0]['TextOverlay']['Lines']
        #words and locations array --> word , top , left
        words_locations =[]
        top =[]
        for i in range(len(lines_arr)):
            words_arr = lines_arr[i]['Words']
            for j in range(len(words_arr)):
                current = words_arr[j] 
                #print words_arr[j]
                #print words_arr[j]['WordText'].encode('utf-8')
                words_locations.append([current['WordText'],current['Top'],current['Left']])
                top.append(current['Top'])
        #print words_locations
        #print top
        TOLERANCE = 24
        same_line = []
        #assuming words that are together comes after each other in the array
        i = 0 #top and words_locations array index
        j = 0 #same_line array index
        while i <= (len(top)-1):
            if (i == (len(top)-1)) and (abs(top[i]-top[i-1])<=TOLERANCE):
                same_line.append([j,words_locations[i][0],words_locations[i][2]])
                break
            if (i == (len(top)-1)) and (abs(top[i]-top[i-1])>TOLERANCE):
                same_line.append([j+1,words_locations[i][0],words_locations[i][2]])
                break
            if abs(top[i]-top[i+1])<=TOLERANCE:
                same_line.append([j,words_locations[i][0],words_locations[i][2]])
                i+=1
            else :
                same_line.append([j,words_locations[i][0],words_locations[i][2]])
                j+=1
                i+=1
            
        return same_line


#Testing
"""
im = cv2.imread('card_out.jpg')
pil_img = Image.fromarray(im)
buff = BytesIO()
pil_img.save(buff, format="JPEG")
new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
OCRSpace('e9925d2b1f88957',new_image_string,OCRSpaceLanguage.Arabic).get_lines()
"""