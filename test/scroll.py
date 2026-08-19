import sys
sys.path.append('src')

from word_api import find_window
import pyautogui
import time

window = find_window()
if window is None:
    print('未找到目标窗口')
    exit()

width = window.width
height = window.height

left_ratio = 0.09
top_ratio = 0.22
right_ratio = 0.78
bottom_ratio = 0.85

left = window.left + int(width * left_ratio)
top = window.top + int(height * top_ratio)
right = window.left + int(width * right_ratio)
bottom = window.top + int(height * bottom_ratio)

crop_height = bottom - top

start_x = (left + right) // 2
start_y = bottom - 10

end_x = (left + right) // 2
end_y = top - 10

try:
    window.activate()
    print('已激活该窗口')
except Exception as e:
    print(f'无法激活窗口: {e}')

time.sleep(0.5)

pyautogui.moveTo(start_x, start_y)
print('尝试滑动...')
time.sleep(0.2)
pyautogui.mouseDown()
pyautogui.moveTo(end_x, end_y, duration=1.0)
pyautogui.mouseUp()