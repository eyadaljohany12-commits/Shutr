from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
from pathlib import Path

app = Flask(__name__)
DOWNLOAD_DIR = Path("Downloads/Shatr")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format_type = data.get('format', 'video') # video, audio, playlist
    speed_limit = data.get('speed_limit', None)
    
    ydl_opts = {
        'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }
    
    if speed_limit:
        ydl_opts['ratelimit'] = int(speed_limit)
        
    if format_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return jsonify({"status": "success", "file": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
