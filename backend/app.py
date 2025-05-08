import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import uuid

# Import your local Whisper, LLM, and TTS modules here
from whisper_model.transcribe import transcribe_audio
from llm_model.ollama_client import ask_llm
from tts_model.coqui_tts import text_to_speech

app = Flask(__name__, static_url_path='', static_folder='static')
from flask_cors import cross_origin
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

UPLOAD_FOLDER = tempfile.gettempdir()

from flask import make_response

@app.route('/api/voice', methods=['POST', 'OPTIONS'])
@cross_origin()
def voice_agent():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        return response, 204

    if 'audio' not in request.files:
        response = jsonify({'error': 'No audio uploaded'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        return response, 400
    audio = request.files['audio']
    temp_audio_path = os.path.join(UPLOAD_FOLDER, f"audio_{uuid.uuid4()}.wav")
    audio.save(temp_audio_path)

    # 1. Speech-to-Text (Whisper)
    try:
        text = transcribe_audio(temp_audio_path)
    except Exception as e:
        text = f"(Whisper error: {e})"

    # 2. LLM Response (Ollama/Llama/Mistral)
    try:
        # Tambahkan konteks untuk LLM
        prompt = f"Berikut adalah percakapan dengan pengguna. Berikan jawaban yang singkat, jelas, dan dalam bahasa Indonesia.\n\nPengguna: {text}\nAI: "
        response_text = ask_llm(prompt, model="llama3")
    except Exception as e:
        response_text = f"Maaf, terjadi error saat menghubungi LLM: {str(e)}"

    # 3. Text-to-Speech (Coqui TTS)
    try:
        # Gunakan Coqui TTS untuk mengubah teks menjadi suara
        audio_response_path = text_to_speech(
            response_text,
            model_name="tts_models/en/ljspeech/tacotron2-DDC"
        )
    except Exception as e:
        # Fallback ke dummy jika TTS gagal
        print(f"TTS Error: {e}")
        audio_response_path = os.path.join(UPLOAD_FOLDER, f"response_{uuid.uuid4()}.wav")
        # Dummy: copy input audio sebagai respons
        with open(temp_audio_path, 'rb') as fin, open(audio_response_path, 'wb') as fout:
            fout.write(fin.read())

    response = make_response(send_file(audio_response_path, mimetype='audio/wav'))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
    return response

@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
