# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, socket
import sys
import datetime
import requests
from io import BytesIO
from PIL import Image
from Adafruit_Thermal import *


ledPin       = 18
buttonPin    = 23
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
dailyFlag    = False # Set after daily trigger occurs
lastId       = '1'   # State information passed to/from interval script
printer      = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)


# Called when button is briefly tapped.  Invokes kitten printing script.
demo_kittens = [
  {
      'screen_name': 'Bodegacats_',
      'image_url': 'https://pbs.twimg.com/media/EaWIqcYX0AA3P3_?format=jpg&name=large',
      'date': datetime.date(2012, 6, 12),
      'text': ""
  },
  {
      'screen_name': 'filzballjaeger',
      'image_url': 'https://pbs.twimg.com/media/EaPiTnXXQAAYWUT?format=jpg&name=large',
      'date': datetime.date(2012, 6, 11),
      'text': "I did nothing all day. It’s exhausting...🐾 #FluffyFursday #CatsOfTwitter"
  },
  {
      'screen_name': 'Indie_TheBengal',
      'image_url': 'https://pbs.twimg.com/media/EaVz58OXsAgRtrB?format=jpg&name=large',
      'date': datetime.date(2012, 6, 12),
      'text': "Finally persuaded my parents that I’m old enough to have my own twitter account... So, hi everyone! I’m Indiana Jones, but my friends call me Indie! #CatsOfTwitter #kitten"
  }
]

def kitten_demo_print(fake_tweet):
  printer.boldOn()
  printer.println(f"@{fake_tweet['screen_name']}")
  printer.boldOff()
  printer.println(fake_tweet['date'].strftime('%b %d %Y'))

  response = requests.get(fake_tweet['image_url'])
  img = Image.open(BytesIO(response.content))
  img.thumbnail((384, 384))
  img.save('temp_img.jpg')

  printer.printImage('temp_img.jpg')

  printer.feed(6)

def tap():
  GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
  kitten = demo_kittens.pop()
  kitten_demo_print(kitten)
  GPIO.output(ledPin, GPIO.LOW)


# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  GPIO.output(ledPin, GPIO.HIGH)
  printer.printImage('gfx/goodbye.png', True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  GPIO.output(ledPin, GPIO.LOW)

# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(30)

# Show IP address (if network is available)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	printer.print('My IP address is ' + s.getsockname()[0])
	printer.feed(3)
except:
	printer.boldOn()
	printer.println('Network is unreachable.')
	printer.boldOff()
	printer.print('Connect display and keyboard\n'
	  'for network troubleshooting.')
	printer.feed(3)
	exit(0)

# Print greeting image
printer.printImage('gfx/hello.png', True)
printer.feed(3)
GPIO.output(ledPin, GPIO.LOW)

# Poll initial button state and time
prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()
tapEnable       = False
holdEnable      = False

# Main loop
while(True):

  # Poll current button state and time
  buttonState = GPIO.input(buttonPin)
  t           = time.time()

  # Has button state changed?
  if buttonState != prevButtonState:
    prevButtonState = buttonState   # Yes, save new state/time
    prevTime        = t
  else:                             # Button state unchanged
    if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
      # Yes it has.  Is the hold action as-yet untriggered?
      if holdEnable == True:        # Yep!
        hold()                      # Perform hold action (usu. shutdown)
        holdEnable = False          # 1 shot...don't repeat hold action
        tapEnable  = False          # Don't do tap action on release
    elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
      # Yes.  Debounced press or release...
      if buttonState == True:       # Button released?
        if tapEnable == True:       # Ignore if prior hold()
          tap()                     # Tap triggered (button released)
          tapEnable  = False        # Disable tap and hold
          holdEnable = False
      else:                         # Button pressed
        tapEnable  = True           # Enable tap and hold actions
        holdEnable = True

  # LED blinks while idle, for a brief interval every 2 seconds.
  # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
  # the PWM-related library is a hassle for average users to install
  # right now.  Might return to this later when it's more accessible.
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
    GPIO.output(ledPin, GPIO.HIGH)
  else:
    GPIO.output(ledPin, GPIO.LOW)
