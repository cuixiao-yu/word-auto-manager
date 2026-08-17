from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ocr = None
window = None

def find_window():
    global window
    pass

def capture():
    pass

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
    pass

@app.route('/scan_once', methods=['GET'])
def scan_once_handler():
    pass

@app.route('/scan_all', methods=['GET'])
def scan_all_handler():
    pass

if __name__ == '__main__':
    print('=' * 50)
    print('API is running...')
    print("=" * 50)

    print('Successfully Running!\n http://localhost:5000')
    print("API list:")
    print("  GET /api-check")
    print("  GET /window")
    print("  GET /scan_once")
    print("  GET /scan_all")
    print("=" * 50)

    app.run(host='localhost', port=5000, debug=False)