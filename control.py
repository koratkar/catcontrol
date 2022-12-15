from gpiozero import AngularServo
from time import sleep
from PIL import Image
import cv2
import web
import os

servo_1 = AngularServo(27, min_angle=0, max_angle=180) # top servo
servo_2 = AngularServo(17, min_angle=0, max_angle=180) # bottom servo

cam = cv2.VideoCapture(0)

urls = (
    '/', 'index',
    '/coords?', 'coords',
    '/image.png', 'image'
)

class index:
  def GET(self):
    raise web.seeother('/static/index.html') 

class coords:
  def GET(self):
    try: 
      user_data = web.input()
      x = user_data.x
      y = user_data.y
      servo_1.angle = round(180 - (x * (180 / 1080)))
      servo_2.angle = round(180 - (y * (180 / 720)))
    except:
      return("no data")

class image:
  def GET(self):
    # possible improvement: return cv2 camera output directly
    img = cam.read()[1]
    cv2.imwrite("image.jpeg", img)
    imageBinary = open("image.png",'rb').read()
    return imageBinary

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()
