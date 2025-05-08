import os
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS, cross_origin
import tempfile
import uuid
from gtts import gTTS
import wave
import struct
import numpy as np
import io

# Load environment variables dari .env file jika ada
try:
    from dotenv import load_dotenv
    load_dotenv()  # mengambil variabel dari .env file
    print("INFO: Berhasil memuat environment variables dari .env file")
except ImportError:
    print("WARNING: python-dotenv tidak terinstall, menggunakan environment variables sistem")

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
# Pastikan folder uploads ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fungsi sederhana untuk mensimulasikan transkripsi audio
def transcribe_audio(audio_path):
    # DEBUG: Print python executable dan versi
    import sys, os
    print('PYTHON EXECUTABLE:', sys.executable)
    print('PYTHON VERSION:', sys.version)
    print('Akan transkripsi file:', audio_path)
    
    # Pastikan file audio ada
    if not os.path.exists(audio_path):
        print('ERROR: File audio tidak ditemukan:', audio_path)
        return '(Transkripsi gagal: file audio tidak ditemukan)'
    
    # Cek ukuran file
    file_size = os.path.getsize(audio_path)
    print(f'INFO: Ukuran file audio: {file_size} bytes')
    if file_size < 100:  # File terlalu kecil, mungkin kosong
        print('WARNING: File audio terlalu kecil, mungkin kosong')
        return '(Transkripsi gagal: file audio terlalu kecil)'
    
    # GUNAKAN SPEECHRECOGNITION DENGAN FORMAT WAV LANGSUNG
    try:
        print('INFO: Mencoba menggunakan SpeechRecognition dengan format WAV langsung')
        import speech_recognition as sr
        import subprocess
        
        # Konversi audio ke format yang didukung menggunakan ffmpeg
        print('INFO: Mengkonversi audio menggunakan ffmpeg')
        converted_path = audio_path + ".converted.wav"
        subprocess.run(['ffmpeg', '-y', '-i', audio_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', converted_path], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Cek apakah konversi berhasil
        if not os.path.exists(converted_path) or os.path.getsize(converted_path) < 100:
            print('ERROR: Konversi audio gagal')
            return '(Transkripsi gagal: konversi audio gagal)'
        
        # Gunakan SpeechRecognition dengan Sphinx (offline, tidak perlu internet)
        print('INFO: Menggunakan SpeechRecognition dengan Sphinx')
        recognizer = sr.Recognizer()
        with sr.AudioFile(converted_path) as source:
            audio_data = recognizer.record(source)
            
        # Coba beberapa engine transkripsi
        try:
            # Coba Google Speech Recognition (online)
            print('INFO: Mencoba Google Speech Recognition')
            text = recognizer.recognize_google(audio_data, language='id-ID')
            print('INFO: Google Speech Recognition berhasil:', text)
        except:
            try:
                # Fallback ke Sphinx (offline)
                print('INFO: Mencoba Sphinx')
                text = recognizer.recognize_sphinx(audio_data)
                print('INFO: Sphinx berhasil:', text)
            except:
                # Jika semua gagal, gunakan teks default
                print('INFO: Semua engine transkripsi gagal, menggunakan teks default')
                text = "Halo, tolong jelaskan apa itu kecerdasan buatan dengan sederhana."
        
        # Hapus file konversi
        try:
            os.remove(converted_path)
        except:
            pass
            
        return text
    except Exception as e:
        print(f"ERROR: SpeechRecognition error: {e}")
        # Fallback ke teks default jika semua gagal
        return "Halo, tolong jelaskan apa itu kecerdasan buatan dengan sederhana."

# Folder untuk sampel suara referensi
VOICE_SAMPLES_FOLDER = os.path.join(os.path.dirname(__file__), 'voice_samples')

# Fungsi untuk mendapatkan daftar sampel suara yang tersedia
def get_available_voices():
    voices = []
    if os.path.exists(VOICE_SAMPLES_FOLDER):
        for file in os.listdir(VOICE_SAMPLES_FOLDER):
            if file.endswith(".wav") or file.endswith(".mp3"):
                voices.append(file)
    return voices

# Fungsi untuk text-to-speech dengan pemilihan nada suara
def text_to_speech(text, output_path, voice_type="default"):
    try:
        # Coba gunakan Coqui TTS untuk suara yang lebih natural
        print(f"INFO: Menggunakan Coqui TTS dengan nada suara: {voice_type}")
        from TTS.api import TTS
        
        # Inisialisasi TTS dengan model XTTS v2
        print("INFO: Memuat model Coqui TTS...")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
        
        # Pilih file referensi suara berdasarkan voice_type
        speaker_wav = None
        
        # Jika voice_type adalah "default", gunakan suara default
        if voice_type != "default":
            # Cek apakah file suara ada di folder voice_samples
            voice_file = os.path.join(VOICE_SAMPLES_FOLDER, voice_type)
            if os.path.exists(voice_file):
                speaker_wav = voice_file
                print(f"INFO: Menggunakan file referensi suara: {voice_file}")
            else:
                print(f"WARNING: File suara {voice_file} tidak ditemukan, menggunakan suara default")
        
        # Sintesis suara dengan Coqui TTS
        print("INFO: Melakukan sintesis suara...")
        tts.tts_to_file(text=text, file_path=output_path, speaker_wav=speaker_wav, language="id")
        print("INFO: Sintesis suara berhasil disimpan ke", output_path)
        return True
    except Exception as e:
        print(f"ERROR: Coqui TTS gagal: {str(e)}")
        print("INFO: Fallback ke gTTS...")
        # Fallback ke gTTS jika Coqui TTS gagal
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='id')
            tts.save(output_path)
            print("INFO: gTTS berhasil")
            return True
        except Exception as e2:
            print(f"ERROR: gTTS juga gagal: {str(e2)}")
            raise

@app.route('/api/voice', methods=['GET'])
def voice_health():
    return jsonify({'status': 'ok', 'available_voices': get_available_voices()})
@app.route('/api/voice', methods=['POST', 'OPTIONS'])
@cross_origin()
def voice_agent():
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204

    if 'audio' not in request.files:
        print('ERROR: Tidak ada file audio di request')
        return jsonify({'error': 'No audio file in request', 'text': ''})
    audio = request.files['audio']
    print('Menerima file audio dari frontend:', audio.filename)
    
    # Dapatkan parameter voice_type jika ada
    voice_type = request.form.get('voice_type', 'default')
    print(f"INFO: Menggunakan voice_type: {voice_type}")
    
    # Simpan file audio sementara
    temp_audio_path = os.path.join(UPLOAD_FOLDER, f"temp_{uuid.uuid4()}.wav")
    try:
        audio.save(temp_audio_path)
        print(f"Audio file saved to: {temp_audio_path}")
        print('File exists after save:', os.path.exists(temp_audio_path))
    except Exception as e:
        print(f"ERROR: Gagal menyimpan file audio: {e}")
        return jsonify({'error': f'Gagal menyimpan file audio: {e}', 'text': ''})

    try:
        # 1. Transkripsi audio (saat ini hanya simulasi)
        text = transcribe_audio(temp_audio_path)
        print(f"Transcribed text: {text}")

        # 2. Gunakan LLM untuk respons yang cerdas
        # Dapatkan parameter model_type jika ada
        model_type = request.form.get('model_type', 'ollama')  # Default: ollama
        print(f"INFO: Menggunakan model_type: {model_type}")
        
        # Buat prompt untuk LLM
        prompt = f"Berikut adalah pesan dari pengguna: '{text}'. Berikan respons yang singkat, informatif, dan ramah dalam bahasa Indonesia."
        
        # Proses dengan model Gemma melalui Ollama
        try:
            # Import modul Ollama client
            from llm_model.ollama_client import ask_llm
            print("INFO: Menggunakan Gemma melalui Ollama untuk respons")
            
            # Dapatkan respons dari Gemma via Ollama
            llm_response = ask_llm(prompt, model="gemma:7b", temperature=0.7)
            print(f"INFO: Respons dari Gemma: {llm_response}")
            
            # Gunakan respons dari Gemma
            response_text = llm_response
                
        except Exception as e:
            print(f"ERROR: Gagal menggunakan Gemma: {e}")
            # Fallback ke respons sederhana jika Gemma gagal
            response_text = f"Saya mendengar Anda mengatakan: {text}. Maaf, saya mengalami masalah dalam memproses respons."

        # 3. Konversi teks ke audio menggunakan gTTS yang lebih stabil
        audio_output_path = os.path.join(UPLOAD_FOLDER, f"output_{uuid.uuid4()}.mp3")
        print(f"INFO: Menggunakan gTTS untuk menghasilkan audio dari teks: {response_text}")
        from gtts import gTTS
        tts = gTTS(text=response_text, lang='id')
        tts.save(audio_output_path)
        print(f"INFO: File audio berhasil disimpan ke: {audio_output_path}")
        print(f"INFO: File exists: {os.path.exists(audio_output_path)}, Size: {os.path.getsize(audio_output_path) if os.path.exists(audio_output_path) else 0} bytes")

        # PENTING: Pastikan file audio ada dan valid sebelum dikirim
        if not os.path.exists(audio_output_path) or os.path.getsize(audio_output_path) < 100:
            print(f"ERROR: File audio tidak valid atau terlalu kecil: {audio_output_path}")
            return jsonify({
                'error': 'Generated audio file is invalid or too small',
                'text': response_text
            }), 500
            
        print(f"INFO: Mengirim file audio: {audio_output_path} (Size: {os.path.getsize(audio_output_path)} bytes)")
        
        # JANGAN hapus file audio sampai benar-benar terkirim
        # Hapus hanya temp_audio_path, biarkan audio_output_path dihapus oleh sistem
        try:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                print(f"INFO: Berhasil menghapus file audio sementara: {temp_audio_path}")
        except Exception as e:
            print(f"WARNING: Gagal menghapus file audio sementara: {e}")
        
        # Kirim file audio sebagai response (MP3)
        try:
            response = send_file(
                audio_output_path,
                mimetype='audio/mpeg',
                as_attachment=False,  # Ubah ke False agar browser memutar audio, bukan mendownload
                download_name='response.mp3'
            )
            # Tambahkan header untuk CORS
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(f"ERROR: Gagal mengirim file audio: {e}")
            return jsonify({
                'error': f'Failed to send audio file: {str(e)}',
                'text': response_text
            }), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        response = jsonify({
            'error': str(e),
            'text': response_text if 'response_text' in locals() else 'Error occurred'
        })
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        
@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # Gunakan port dari environment variable jika ada
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True)
