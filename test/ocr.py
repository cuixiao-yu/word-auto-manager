import sys
sys.path.append('src')

from word_api import capture, extract

img = capture()

if img:
    texts = extract(img)
    for i, text in enumerate(texts):
        print(f'  {i+1}: {text}')