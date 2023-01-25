from gpiozero import AngularServo
from time import sleep
from PIL import Image
import cv2
import web
import os

servo_1 = AngularServo(27, min_angle=0, max_angle=180) # top servo
servo_2 = AngularServo(17, min_angle=0, max_angle=180) # bottom servo

cam = cv2.VideoCapture(0)

def coord_to_x_angle(x):
    return round(180 - (x * (180 / 1080)))

def coord_to_y_angle(y):
    return round(180 - (y * (180 / 720)))

def set_angle_choppy(x, y):
    x_old = servo_1.angle
    y_old = servo_2.angle
    x_diff = abs(x - x_old)
    y_diff = abs(y - y_old)
    for i in range(10,1,-1):
        servo_1.angle = coord_to_x(x_old + round(x_diff / i))
        servo_2.angle = coord_to_y(y_old + round(y_diff / i))
    
    

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
      
      set_angle_choppy(x, y)
      
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
