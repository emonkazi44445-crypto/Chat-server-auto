import requests
import threading
import time
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# তোমার বট ডিটেইলস
BOT_TOKEN = "8427068930:AAGSygGuAfl27uEkJjOxQXWOouX3XQM0unI"
CHAT_ID = "6421195166"

# --- ব্যাকগ্রাউন্ড কাজ: ১ মিনিট পর পর লগ দেখাবে ---
def server_logs():
    while True:
        # বর্তমান সময়সহ লগ প্রিন্ট করবে
        current_time = time.strftime("%H:%M:%S")
        print(f"[{current_time}] সার্ভার সচল আছে এবং কাজ করছে...")
        
        # ৬০ সেকেন্ড বা ১ মিনিট অপেক্ষা করবে
        time.sleep(300)

@app.route('/upload', methods=['POST'])
def upload_to_telegram():
    file = request.files.get('file')
    if not file: return jsonify({"ok": False}), 400

    is_video = file.content_type.startswith('video/')
    method = "sendVideo" if is_video else "sendPhoto"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    files = {'video' if is_video else 'photo': (file.filename, file.read(), file.content_type)}
    
    try:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files=files).json()
        return jsonify(response)
    except:
        return jsonify({"ok": False}), 500

@app.route('/stream/<file_id>')
def stream(file_id):
    if "." in file_id: return "Invalid File", 404
    res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
    if res.get("ok"):
        return redirect(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}")
    return "Not Found", 404

if __name__ == '__main__':
    # সার্ভার শুরু হওয়ার আগে ব্যাকগ্রাউন্ড থ্রেডটি চালু করছি
    # daemon=True দেওয়ার কারণ হলো মেইন সার্ভার বন্ধ করলে এটাও বন্ধ হয়ে যাবে
    threading.Thread(target=server_logs, daemon=True).start()
    
    # ফ্লাস্ক অ্যাপ রান করা হচ্ছে
    app.run(host='0.0.0.0', port=5000)
