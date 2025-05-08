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
from tts_model.audio_enhancer import enhance_audio_quality

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
        # Jika semua gagal, return string kosong agar backend bisa deteksi error
        print("ERROR: Semua engine transkripsi gagal. Tidak ada hasil transkripsi.")
        return ""

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
    """
    Mengubah teks menjadi ucapan dan menyimpannya ke file.
    """
    # Selalu gunakan TTS default (misal gTTS Bahasa Indonesia)
    try:
        print(f"INFO: Menggunakan gTTS untuk menghasilkan audio default Bahasa Indonesia")
        from gtts import gTTS
        tts = gTTS(text=text, lang='id', tld='co.id')
        tts.save(output_path)
        print(f"INFO: File audio berhasil disimpan ke: {output_path}")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
        
        # Pilih file referensi suara berdasarkan voice_type
        speaker_wav = None
        
        # Tentukan file sampel suara berdasarkan voice_type
        speaker_wav = None
        if voice_type == "duwi":
            # Gunakan file duwi.wav
            duwi_sample = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_samples", "duwi.wav")
            if os.path.exists(duwi_sample):
                speaker_wav = duwi_sample
                print(f"INFO: Menggunakan sampel suara: {duwi_sample}")
            else:
                print("WARNING: File duwi.wav tidak ditemukan, menggunakan suara default")
                # Fallback ke default
                voice_type = "default"
                
        if voice_type == "default":
            # Coba gunakan file default_male.wav jika ada
            default_male = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_samples", "default_male.wav")
            if os.path.exists(default_male):
                speaker_wav = default_male
            else:
                # Jika tidak ada, gunakan default dari model
                print("WARNING: File default_male.wav tidak ditemukan, menggunakan suara default")
        elif voice_type != "elevenlabs":  # Skip jika voice_type adalah elevenlabs
            # Cek apakah file suara ada di folder voice_samples
            voice_file = os.path.join(VOICE_SAMPLES_FOLDER, voice_type)
            if os.path.exists(voice_file):
                speaker_wav = voice_file
                print(f"INFO: Menggunakan file referensi suara: {voice_file}")
            else:
                print(f"WARNING: File suara {voice_file} tidak ditemukan, menggunakan suara default")
                # Coba gunakan sampel suara default
                default_sample = os.path.join(VOICE_SAMPLES_FOLDER, "default_male.wav")
                if os.path.exists(default_sample):
                    speaker_wav = default_sample
                    print(f"INFO: Menggunakan file referensi suara default: {default_sample}")
        
        # Sintesis suara dengan Coqui TTS
        print("INFO: Melakukan sintesis suara...")
        
        # Tambahkan parameter untuk membuat suara lebih natural
        if speaker_wav:
            # Gunakan sampel suara dengan pengaturan tambahan
            if voice_type == "duwi":
                # Pengaturan khusus untuk suara Duwi
                tts.tts_to_file(
                    text=processed_text, 
                    file_path=output_path, 
                    speaker_wav=speaker_wav, 
                    language="id",
                    # Pengaturan optimal untuk suara Duwi
                    speed=0.92,  # Sedikit lebih lambat untuk kejelasan
                    temperature=0.8,  # Lebih tinggi untuk variasi yang lebih natural
                    # Pengaturan tambahan untuk suara Duwi
                    speaker_wav_volume_adjust=True,  # Otomatis menyesuaikan volume
                    speaker_wav_silence_padding=0.2  # Tambahkan padding untuk hasil lebih baik
                )
                print("INFO: Menggunakan pengaturan khusus untuk suara Duwi")
            else:
                # Pengaturan default untuk sampel suara lainnya
                tts.tts_to_file(
                    text=processed_text, 
                    file_path=output_path, 
                    speaker_wav=speaker_wav, 
                    language="id",
                    # Tambahkan pengaturan untuk suara lebih natural
                    speed=0.95,  # Sedikit lebih lambat untuk kejelasan
                    temperature=0.75  # Lebih tinggi untuk variasi yang lebih natural
                )
            
            # Post-process audio untuk meningkatkan kualitas
            enhance_audio_quality(output_path)
            
        else:
            # Jika tidak ada sampel suara, gunakan suara bawaan dengan pengaturan default
            tts.tts_to_file(
                text=processed_text, 
                file_path=output_path, 
                language="id",
                # Tambahkan pengaturan untuk suara lebih natural
                speed=0.95,  # Sedikit lebih lambat untuk kejelasan
                temperature=0.75  # Lebih tinggi untuk variasi yang lebih natural
            )
            
            # Post-process audio untuk meningkatkan kualitas
            enhance_audio_quality(output_path)
            
        print("INFO: Sintesis suara berhasil disimpan ke", output_path)
        return True
    except Exception as e:
        print(f"ERROR: Coqui TTS gagal: {str(e)}")
        print("INFO: Fallback ke gTTS...")
        # Fallback ke gTTS jika Coqui TTS gagal
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='id', tld='co.id')
            tts.save(output_path)
            print("INFO: gTTS berhasil")
            return True
        except Exception as e2:
            print(f"ERROR: gTTS juga gagal: {str(e2)}")
            return False

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
        
        # Jika hasil transkripsi kosong, kembalikan error ke frontend
        if not text or text.strip() == "":
            print("ERROR: Transkripsi audio gagal. Tidak ada input valid untuk AI.")
            return jsonify({
                'error': 'Transkripsi audio gagal. Silakan ulangi rekaman Anda.',
                'text': ''
            }), 400

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

        # 3. Konversi teks ke audio menggunakan fungsi text_to_speech dengan sampel suara
        # Jika voice_type == "duwi", gunakan output .wav lalu convert ke .mp3
        if voice_type == "duwi":
            wav_output_path = os.path.join(UPLOAD_FOLDER, f"output_{uuid.uuid4()}.wav")
            print(f"DEBUG: Memanggil text_to_speech dengan voice_type=duwi, output_path={wav_output_path}")
            success = text_to_speech(response_text, wav_output_path, voice_type=voice_type)
            if success:
                # Convert wav ke mp3 untuk frontend
                try:
                    import subprocess
                    mp3_output_path = os.path.join(UPLOAD_FOLDER, f"output_{uuid.uuid4()}.mp3")
                    subprocess.run(["ffmpeg", "-y", "-i", wav_output_path, mp3_output_path], check=True)
                    audio_output_path = mp3_output_path
                    print(f"INFO: File audio berhasil dikonversi ke: {audio_output_path}")
                except Exception as e:
                    print(f"ERROR: Konversi wav ke mp3 gagal: {e}")
                    audio_output_path = wav_output_path
            else:
                print("WARNING: text_to_speech gagal, fallback ke gTTS")
                audio_output_path = os.path.join(UPLOAD_FOLDER, f"output_{uuid.uuid4()}.mp3")
                from gtts import gTTS
                tts = gTTS(text=response_text, lang='id', tld='co.id')
                tts.save(audio_output_path)
        else:
            # Untuk selain duwi, tetap gunakan mp3/gTTS jika perlu
            audio_output_path = os.path.join(UPLOAD_FOLDER, f"output_{uuid.uuid4()}.mp3")
            print(f"DEBUG: Memanggil text_to_speech dengan voice_type={voice_type}, output_path={audio_output_path}")
            success = text_to_speech(response_text, audio_output_path, voice_type=voice_type)
            if not success:
                print("WARNING: text_to_speech gagal, fallback ke gTTS")
                audio_output_path = os.path.join(UPLOAD_FOLDER, f"output_{uuid.uuid4()}.mp3")
                from gtts import gTTS
                tts = gTTS(text=response_text, lang='id', tld='co.id')
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
        
        # Kirim file audio sebagai response
        try:
            # Tentukan MIME type yang benar berdasarkan ekstensi file
            if audio_output_path.endswith('.wav'):
                mimetype = 'audio/wav'
                download_name = "response.wav"
            else:
                mimetype = 'audio/mpeg'
                download_name = "response.mp3"
                
            print(f"INFO: Mengirim file audio dengan MIME type: {mimetype}")
            response = send_file(
                audio_output_path,
                mimetype=mimetype,
                as_attachment=False,  # False agar browser memutar audio, bukan mendownload
                download_name=download_name
            )
            # Tambahkan header untuk CORS
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            print(f"ERROR: Gagal mengirim file audio: {str(e)}")
            return jsonify({
                'error': 'Failed to send audio file',
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
    # Tetapkan port 5053 secara eksplisit
    port = 5053
    print(f"INFO: Menjalankan aplikasi di port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
