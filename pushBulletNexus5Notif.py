import urllib2
import re
import os.path
import requests
import json
from bs4 import BeautifulSoup

def send_notif(device_codename, device_name, channel_name, image_name):
   url = 'https://api.pushbullet.com/v2/pushes'
   payload = {'channel_tag': channel_name, 'type': 'link', 'body': 'Android ' + image_name + ' for ' + device_name + ' released! Go grab it!', 'Title' : 'New Factory image for ' + device_name + '!', 'url' : 'https://developers.google.com/android/nexus/images#' + device_codename}
   headers = {'Content-Type' : 'application/json', 'Authorization': 'Basic <yout_token_here>=='}
   r = requests.post(url, data=json.dumps(payload), headers=headers)


devices =       {'hammerhead' : {'name': 'Nexus 5', 'channel' : 'nexus5updates'},
                'bullhead' : {'name': 'Nexus 5X', 'channel' : 'nexus5xupdates'},
                'angler' : {'name': 'Nexus 6P', 'channel' : 'nexus6pupdates'}}


for codename, device in devices.iteritems():
   FILE_PATH = './number_of_images_' + codename + '.dat'
   prev_images=''

   if os.path.isfile(FILE_PATH):
      fh = open(FILE_PATH, 'r')
      prev_images = fh.read()
      fh.close()

   if prev_images == '':
      prev_images='0'
   print prev_images
   page = urllib2.urlopen('https://developers.google.com/android/nexus/images').read()
   soup = BeautifulSoup(page)
   images_rows = soup.find_all('tr',id=re.compile(codename + '.+'))
   current_images = len(images_rows)
   print current_images
   last_image_name = images_rows[-1].find_all('td')[0].get_text()
   if current_images > int(prev_images):
      send_notif(codename, device['name'], device['channel'], last_image_name)
      fh = open(FILE_PATH, 'w+')
      fh.write(str(current_images))
      print 'new_image'
      fh.close()
   print last_image_name
   print codename, device['name'], device['channel']
