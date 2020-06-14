
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

more_fake_tweets = [
    {
        'screen_name': 'Alabama',
        'image_url': 'http://www.google.com',
        'date': datetime.datetime.today(),
        'text': "This is the first fake tweet"
    },
    {
        'screen_name': 'California',
        'image_url': 'http://www.bing.com',
        'date': datetime.datetime.today(),
        'text': "This is the second fake tweet"
    },
    {
        'screen_name': 'Delaware',
        'image_url': 'http://www.yahoo.com',
        'date': datetime.datetime.today(),
        'text': "This is the third fake tweet"
    }
]

printer.boldOn()
printer.println(f"@{fake_tweet['screen_name']}")
printer.boldOff()
printer.println(fake_tweet['date'].strftime('%b %d %Y'))

response = requests.get(fake_tweet['image_url'])
img = Image.open(BytesIO(response.content))
img.thumbnail((384, 384))
img.save('temp_img.jpg')

printer.printImage('temp_img.jpg')

printer.feed(3)
