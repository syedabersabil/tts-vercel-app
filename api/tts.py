import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import edge_tts
import asyncio
import tempfile

VOICES = {
    "hi_female": "hi-IN-SwaraNeural",
    "hi_male": "hi-IN-MadhurNeural",
    "en_in_female": "en-IN-NeerjaNeural",
    "en_in_male": "en-IN-PrabhatNeural",
    "en_us_female": "en-US-AriaNeural",
    "en_us_male": "en-US-GuyNeural",
}

async def generate_tts(text, voice_key, rate, pitch):
    voice = VOICES.get(voice_key, "hi-IN-SwaraNeural")
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    output_file = temp_file.name
    temp_file.close()

    communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    await communicate.save(output_file)

    with open(output_file, "rb") as f:
        audio_data = f.read()

    os.remove(output_file)
    return audio_data

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            text = data.get("text", "").strip()
            voice = data.get("voice", "hi_female")
            rate = int(data.get("rate", 0))
            pitch = int(data.get("pitch", 0))

            if not text:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Text is required"}).encode("utf-8"))
                return

            audio_data = asyncio.run(generate_tts(text, voice, rate, pitch))

            self._set_headers(200, "audio/mpeg")
            self.wfile.write(audio_data)

        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
