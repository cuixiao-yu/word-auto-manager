import sys
sys.path.append('src')

from word_api import capture, crop_word

img = capture()

if img:
    cropped = crop_word(img)