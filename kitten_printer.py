import sys
import datetime
import requests
from Adafruit_Thermal import *
from PIL import Image
from io import BytesIO
from kitten_retrieval import *

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

def print_a_kitten():
    cute_tweet = pick_new_kitten(search_tweets())
    if not cute_tweet:
        printer.println('Sorry, no new kittens. :(')
        printer.println('Please try again later.')
    else:
        response = requests.get(cute_tweet['image_url'])
        img = Image.open(BytesIO(response.content))
        img.thumbnail((384, 384))
        img.save('temp_img.jpg')

        printer.boldOn()
        printer.println("@" + cute_tweet['screen_name'])
        printer.boldOff()
        printer.println(cute_tweet['date'].strftime('%b %d %Y'))
        printer.printImage('temp_img.jpg')

printer.feed(3)

