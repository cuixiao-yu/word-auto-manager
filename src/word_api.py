from flask import Flask, jsonify
from flask_cors import CORS
import pygetwindow as gw
from PIL import Image, ImageGrab
import ctypes
import easyocr
import numpy as np
import cv2

app = Flask(__name__)
CORS(app)

reader = None
window = None

def find_window():
    global window
    windows = gw.getAllWindows()
    for w in windows:
        title = w.title
        if not title:
            continue
        if 'vivoScreen' in title:
            window = w
            print(f'找到目标窗口: "{title}"')
            return window
    print('未找到目标窗口，请确保:')
    print('  1. vivo 办公套件已打开')
    print('  2. 手机已连接')
    print('  3. 已打开投屏窗口')
    return None

def capture():
    global window
    window = find_window()
    if window is None:
        print('未找到目标窗口，无法截图')
        return None
    else:
        try:
            window.activate()
            print("已激活该窗口")
        except Exception as e:
            print(f'无法激活窗口: {e}')
        
        factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        left = int(window.left * factor)
        top = int(window.top * factor)
        width = int(window.width * factor)
        height = int(window.height * factor)

        print(f'缩放比例: {factor}')
        print(f'窗口信息: left={left}, top={top}, width={width}, height={height}')

        screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))
        screenshot.save('outfile/screenshot.png')
        print('截图已保存: outfile/screenshot.png')

        return screenshot

def pre_process(image):
    img_arr = np.array(image)
    
    gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
    
    binary = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    kernel = np.ones((1, 1), np.uint8)
    denoised = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    processed = Image.fromarray(denoised)
    
    processed.save('outfile/preprocessed.png')
    print("预处理完成，已保存: outfile/preprocessed.png")
    
    return processed

def crop_word(image):
    width, height = image.size
    
    left = int(width * 0.08)
    top = int(height * 0.22)
    right = int(width * 0.77)
    bottom = int(height * 0.84)
    
    cropped = image.crop((left, top, right, bottom))
    
    print(f'裁剪区域: left={left}, top={top}, right={right}, bottom={bottom}')
    print(f'裁剪尺寸: {cropped.width} x {cropped.height}')
    
    cropped.save('outfile/cropped.png')
    print("已保存: outfile/cropped.png")
    
    return cropped

def init_ocr():
    global reader

    print("正在初始化 OCR 引擎...")
    reader = easyocr.Reader(['ch_sim', 'en'], gpu = False)
    print("初始化完成!")

    return reader

def extract(image):
    global reader
    reader = init_ocr()
    
    cropped = crop_word(image)
    processed = pre_process(cropped)

    img_arr = np.array(processed)
    
    res = reader.readtext(img_arr)
    
    texts = [item[1] for item in res]
    print(f'共识别到 {len(texts)} 段文字')
    return texts

def parse_word_line(text):
    pass

def filter_and_parse(texts):
    pass

def scroll():
    global window
    pass

def scan_once():
    pass

def scan_all(max_pages=50):
    pass

@app.route('/api-check', methods=['GET'])
def running_check():
    return jsonify({"status": "ok"})

@app.route('/window', methods=['GET'])
def window_info_handler():
    global window
    window = find_window()
    if window is None:
        return jsonify({
            "found": False,
            "message": "未找到目标窗口"
        })
    else:
        return jsonify({
            "found": True,
            "title": window.title,
            "left": window.left,
            "top": window.top,
            "width": window.width,
            "height": window.height,
            "is_minimized": window.isMinimized,
            "is_active": window.isActive
        })

@app.route('/scan_once', methods=['GET'])
def scan_once_handler():
    pass

@app.route('/scan_all', methods=['GET'])
def scan_all_handler():
    pass

if __name__ == '__main__':
    print('=' * 50)
    print('API 服务器启动中...')
    print("=" * 50)

    print('启动成功!\n监听地址: http://localhost:5000')
    print("API 接口:")
    print("  GET /api-check")
    print("  GET /window")
    print("  GET /scan_once")
    print("  GET /scan_all")
    print("=" * 50)

    app.run(host='localhost', port=5000, debug=False)