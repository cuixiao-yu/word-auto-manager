from flask import Flask, jsonify
from flask_cors import CORS
import pygetwindow as gw
from PIL import ImageGrab
import ctypes

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

def pre_process(image):
    pass

def crop_word(image):
    pass

def extract(image):
    pass

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