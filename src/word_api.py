from flask import Flask, jsonify
from flask_cors import CORS
import pygetwindow as gw
from PIL import ImageGrab
import ctypes
import numpy as np
from paddleocr import PaddleOCR

app = Flask(__name__)
CORS(app)

ocr = None
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
    
    try:
        window.activate()
        print('已激活该窗口')
    except Exception as e:
        print(f'无法激活窗口: {e}')
    
    try:
        factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    except:
        factor = 1.25
    
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

def crop_word(image):
    width, height = image.size
    left = int(width * 0.09)
    top = int(height * 0.22)
    right = int(width * 0.78)
    bottom = int(height * 0.85)
    cropped = image.crop((left, top, right, bottom))
    print(f'裁剪区域: left={left}, top={top}, right={right}, bottom={bottom}')
    print(f'裁剪尺寸: {cropped.width} x {cropped.height}')
    cropped.save('outfile/cropped.png')
    return cropped

def init_ocr():
    global ocr

    print('正在初始化 OCR 引擎...')
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    print('初始化完成!')

    return ocr

def extract(image):
    global ocr
    if ocr is None:
        ocr = init_ocr()
    
    cropped = crop_word(image)
    
    img_array = np.array(cropped)
    result = ocr.ocr(img_array)
    
    texts = []
    for line in result:
        if line is None:
            continue
        for word_info in line:
            text = word_info[1][0]
            confidence = word_info[1][1]
            if confidence > 0.5:
                texts.append(text)
    
    print(f'共识别到 {len(texts)} 段文字')
    return texts

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