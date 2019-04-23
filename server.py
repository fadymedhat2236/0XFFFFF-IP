from flask import Flask, redirect, url_for, request
import cv2
import io
import numpy as np
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      image = request.files['file']    
      in_memory_file = io.BytesIO()
      image.save(in_memory_file)
      data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
      color_image_flag = 1
      img = cv2.imdecode(data, color_image_flag)
      #######here image processing part##########
      cv2.imwrite("data.jpg",img)
      user = request.form['name']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('name')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)