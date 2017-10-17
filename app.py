from flask import Flask, request
from flask_cors import CORS, cross_origin
import base64
from io import StringIO, BytesIO
import cv2
import numpy as np 

app = Flask('Edges')
CORS(app)

def cv_engine(img, operation):
    if operation == 'to_grayscale':
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif operation == 'get_edge_canny':
        print('Canny')
        gray        = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(gray, 100, 200, 3)
        return canny_edges
    elif operation == 'get_edge_sobel':
        gray    = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        x_edges = cv2.Sobel(gray, -1, 1, 0, ksize = 5)
        y_edges = cv2.Sobel(gray, -1, 0, 1, ksize = 5)
        edges   = cv2.addWeighted(x_edges, 0.5, y_edges, 0.5, 0)
        return edges   
    else:
        return None

def read_image(image_data):
    image_data = base64.decodebytes(image_data)
    with open('temp_image.jpg', 'wb') as f:
        f.write(image_data)
        f.close()
    img = cv2.imread('temp_image.jpg')
    return img 

def encode_image(img):
    ret, data = cv2.imencode('.jpg', img)
    return base64.b64encode(data)

# This is the server to handle requests and get images from client
@app.route('/process_image', methods=['POST'])
def process_image():
    if not request.json or 'msg' not in request.json:
        return 'Server Error!', 500

    image_data = request.json['image_data'][23:].encode()
    operation  = request.json['operation']
    print(operation)
    img        = read_image(image_data)
    img_out    = cv_engine(img, operation)
    image_data = encode_image(img_out)
    result     = {'image_data': image_data, 'msg':'Operation Completed'}
    return image_data, 200

@app.route('/')
def index():
    return 'Python is AWESOME!'

if __name__ == '__main__':
    app.run(debug=True)