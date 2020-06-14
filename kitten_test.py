#!/usr/bin/python

import sys
import datetime
import requests
from Adafruit_Thermal import *
from PIL import Image
from io import BytesIO

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

fake_tweet = {
        'screen_name': 'test_kitten',
        'image_url': 'https://cdn.mos.cms.futurecdn.net/vChK6pTy3vN3KbYZ7UU7k3-1200-80.jpg',
        'date': datetime.datetime.today(),
        'text': "This is a test kitten."
}

printer.boldOn()
printer.println(f"@{fake_tweet['screen_name']}")
printer.boldOff()

printer.println(fake_tweet['date'].strftime('%b %d %Y'))

# printer.printImage(Image.open('gfx/hello.png'), True)

response = requests.get(fake_tweet['image_url'])
img = Image.open(BytesIO(response.content))
img.thumbnail((384, 384))
img.save('temp_img.jpg')

printer.printImage(Image.open('temp_img.jpg'))

printer.feed(3)