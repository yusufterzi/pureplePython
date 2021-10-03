from rembg.bg import remove
import numpy as np
import io
from PIL import Image
from flask import Flask,jsonify,make_response,request,Response
from furl import furl
import requests
from flask import request
from gevent.pywsgi import WSGIServer
import resource
from random import randint
import bjoern
import json
import cv2
import jsonpickle
import base64
from io import BytesIO
import io

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))     
app = Flask(__name__)
headers = {'Content-Type': 'application/json; charset=utf-8'}


@app.route("/getImageWithoutBg", methods=['GET','POST'])
def getImageWithoutBg():
    requestJson = request.get_json()
    imgstring = requestJson['inputImage']

    image = Image.open(BytesIO(base64.b64decode(imgstring)))

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    data = np.asarray(img_byte_arr)

    result = remove(data)

    img = Image.open(io.BytesIO(result)).convert("RGBA")

    output = BytesIO()
    img.save(output, format='PNG')
    im_data = output.getvalue()

    image_data = base64.b64encode(im_data)
    if not isinstance(image_data, str):
        image_data = image_data.decode()
    data_url = 'data:image/jpg;base64,' + image_data
    
    return jsonify({ "value" : data_url })

if __name__ == '__main__':
    #http_server = WSGIServer(('',301), app)
    #http_server.serve_forever()
    bjoern.run(app, '', int(80))
    #app.run()
