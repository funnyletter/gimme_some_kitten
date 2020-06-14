# Gimme Some Kitten

Extends and modifies the original Adafruit [Python-Thermal-Printer](https://github.com/adafruit/Python-Thermal-Printer) library so the Raspberry Pi thermal printer will fetch an image of a kitten from twitter and print it when the button is pressed.

Bad day? Kitten. Feeling sad? Kitten. Want to impress your friends? Kitten.

It uses tweepy to search twitter posts and find ones that mention kittens and include media. It then uses requests to get the image and pillow to resize it to an appropriate resolution for a $50 thermal printer. I have shamelessly reused Adafruit's button handling, startup, and shutdown code.

## Known Issues/Future Enhancements

### Not An Actual Kitten
Turns out twitter users use the word "kitten" and then post a photo a lot and the photo is not actually a kitten. Future plans include fiddling the popularity settings and/or accounts searched to optimize for quality kitten content.

REALLY FANCY future plans involve using machine learning to screen images for presence of kittens.
