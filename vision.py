#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import io
import os

from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse

def broken_bike_detection(uri, keyword):

    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r".\googleCred.json"

    with open('bike1.jpg', 'wb') as handle:
            response = requests.get(uri, stream=True)
            if not response.ok:
                print (response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    vision_client = vision.ImageAnnotatorClient()
    file_name = 'bike1.jpg'

    with io.open(file_name,'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    response_json = AnnotateImageResponse.to_json(response)
    response = json.loads(response_json)
    for re in response['labelAnnotations']:
        if re['description'].lower() == keyword:
            return True
    return False

def detect_labels_uri(uri, keyword):

    result = broken_bike_detection(uri, keyword)

    print(result)
    
    return result


    



