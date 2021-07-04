import cv2
from dotenv import dotenv_values
import os
from flask import Flask


temp = dotenv_values(".env")


def gen(video):
    while True:
        _, image = video.read()
        _, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def take_picture(video):    
    _, frame = video.read() 
    cv2.imwrite(os.path.join(temp["UPLOAD_FOLDER"], "current_cam_image.jpg"), frame) 

