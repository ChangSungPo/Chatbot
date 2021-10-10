#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import os
import requests
from google.cloud import vision
from google.cloud.vision_v1 import types

def doorplate_recognition(uri):
    with open('plate1.jpg', 'wb') as handle:
            response = requests.get(uri, stream=True)

            if not response.ok:
                print (response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)


    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r".\googleCred.json"

    vision_client = vision.ImageAnnotatorClient()
    file_name = 'plate1.jpg'

    with io.open(file_name,'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations # string type
    
    string = ''
    length = len(texts)
    if length:
        page = texts[0].description
        page = page.split()
        for i in page:
            string = string + i + ','
    
        return string
    else:
        return None