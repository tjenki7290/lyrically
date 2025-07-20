import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import yt_dlp
from dotenv import load_dotenv
from flask import send_from_directory




load_dotenv()

# Configuration
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5001")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Initialize OpenAI client only if API key is available
if Config.OPENAI_API_KEY:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
else:
    client = None
    print("⚠️  WARNING: OPENAI_API_KEY not set!")




app = Flask(__name__)
app.config.from_object(Config)




# Configure CORS for production
CORS(app, origins=Config.ALLOWED_ORIGINS, supports_credentials=True)




TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.route("/temp/<filename>")
def serve_audio(filename):
   return send_from_directory(TEMP_DIR, filename)




@app.route("/api/ping", methods=["GET"])
def ping():
  return jsonify({"message": "pong"}), 200

@app.route("/health", methods=["GET"])
def health_check():
  return jsonify({"status": "healthy", "service": "lyrically-backend"}), 200




@app.route("/api/transcribe", methods=["POST"])
def transcribe_from_url():
  print("🔁 /api/transcribe hit")
  data = request.get_json()
  url = data.get("url")
  if not url:
      return jsonify({"error": "URL missing"}), 400




  temp_id = str(uuid.uuid4())
  output_base = os.path.join(TEMP_DIR, temp_id)
  mp3_path = f"{output_base}.mp3"
  title = "Unknown Title"




  try:
      ydl_opts = {
          'format': 'bestaudio/best',
          'outtmpl': f"{output_base}.%(ext)s",
          'postprocessors': [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'mp3',
          }],
          'quiet': True,
          'noplaylist': True,
      }




      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(url, download=True)
          title = info.get('title', title)




      if not os.path.exists(mp3_path):
          raise FileNotFoundError("MP3 not created from YouTube")




      if not client:
          return jsonify({"error": "OpenAI API key not configured"}), 500
          
      with open(mp3_path, "rb") as audio_file:
          transcript = client.audio.transcriptions.create(
              model="whisper-1",
              file=audio_file,
          )




      return jsonify({
          "lyrics": transcript.text,
          "title": title,
          "audioUrl": f"{Config.BASE_URL}/temp/{os.path.basename(mp3_path)}"
      })




  except Exception as e:
      print("🔥 URL Error:", e)
      return jsonify({"error": str(e)}), 500




  finally:
      # Clean up the downloaded file after processing
      if os.path.exists(mp3_path):
          try:
              os.remove(mp3_path)
          except Exception as e:
              print(f"Warning: Could not remove {mp3_path}: {e}")




@app.route("/api/upload", methods=["POST"])
def transcribe_uploaded_file():
  print("🎙️ /api/upload hit")
  if "file" not in request.files:
      return jsonify({"error": "No file uploaded"}), 400




  file = request.files["file"]
  if file.filename == "":
      return jsonify({"error": "Empty filename"}), 400

  # Check file size (limit to 50MB)
  file.seek(0, 2)  # Seek to end
  file_size = file.tell()
  file.seek(0)  # Reset to beginning
  
  if file_size > 50 * 1024 * 1024:  # 50MB limit
      return jsonify({"error": "File too large. Maximum size is 50MB."}), 400




  title = os.path.splitext(file.filename)[0]
  temp_id = str(uuid.uuid4())
  mp3_path = os.path.join(TEMP_DIR, f"{temp_id}.mp3")




  try:
      file.save(mp3_path)




      if not client:
          return jsonify({"error": "OpenAI API key not configured"}), 500
          
      with open(mp3_path, "rb") as audio_file:
          transcript = client.audio.transcriptions.create(
              model="whisper-1",
              file=audio_file
          )




      return jsonify({
          "lyrics": transcript.text,
          "title": title,
          "audioUrl": f"{Config.BASE_URL}/temp/{os.path.basename(mp3_path)}"
      })




  except Exception as e:
      print("🔥 Upload Error:", e)
      return jsonify({"error": str(e)}), 500




  finally:
      if os.path.exists(mp3_path):
          os.remove(mp3_path)




if __name__ == "__main__":
  debug_mode = Config.FLASK_ENV == "development"
  port = int(os.environ.get("PORT", 5001))
  app.run(debug=debug_mode, port=port, host="0.0.0.0")



