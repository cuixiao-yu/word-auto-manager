import sys
sys.path.append('src')

from word_api import capture, extract, pre_process

img = capture()

if img:
    texts = extract(img)
    for i, text in enumerate(texts):
        print(f'  {i+1}: {text}')