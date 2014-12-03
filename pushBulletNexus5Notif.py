import urllib2
import re
import os.path
import requests
import json
from bs4 import BeautifulSoup

def send_notif(image_name):
   url = 'https://api.pushbullet.com/v2/pushes'
   payload = {'channel_tag': 'nexus5updates', 'type': 'link', 'body': image_name + ' for Nexus 5 released! Go grab it!', 'Title' : 'New Factory image for Nexus 5!', 'url' : 'https://developers.google.com/android/nexus/images#hammerhead'}
   headers = {'Content-Type' : 'application/json', 'Authorization': 'Basic <your_access_token>=='}
   r = requests.post(url, data=json.dumps(payload), headers=headers)

FILE_PATH = "./number_of_images.dat"
prev_images=""

if os.path.isfile(FILE_PATH):
  fh = open(FILE_PATH, "r")
  prev_images = fh.read()
  fh.close()

if prev_images == "":
   prev_images="0"
print prev_images
page = urllib2.urlopen('https://developers.google.com/android/nexus/images').read()
soup = BeautifulSoup(page)
images_links = soup.find_all(href=re.compile("#hammerhead.+"))
current_images = len(images_links)
print current_images
if current_images > int(prev_images):
   send_notif(images_links[-1].get_text())
   fh = open(FILE_PATH, "w+")
   fh.write(str(current_images))
   print "new_image"
   fh.close()
print images_links[-1].get_text()
