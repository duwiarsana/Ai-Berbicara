import requests
import os
import json

def text_to_speech_elevenlabs(text, output_path, voice_id=None):
    """
    Mengubah teks menjadi ucapan menggunakan ElevenLabs API.
    
    Args:
        text (str): Teks yang akan diubah menjadi ucapan
        output_path (str): Path untuk menyimpan file audio output
        voice_id (str): ID suara yang akan digunakan (default: dari env variable)
        
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        # Dapatkan API key dari environment variable
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            print("ERROR: ELEVENLABS_API_KEY tidak ditemukan di environment variables")
            return False
            
        # Dapatkan voice ID dari environment variable jika tidak ditentukan
        if not voice_id:
            voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Default: Suara Indonesia
        
        # Import text processor untuk meningkatkan kualitas suara
        from tts_model.text_processor import preprocess_text_for_tts
        
        # Proses teks untuk meningkatkan intonasi
        processed_text = preprocess_text_for_tts(text)
        print(f"INFO: Teks setelah preprocessing: {processed_text[:100]}...")
            
        # URL endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        # Headers
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        # Deteksi jika teks menggunakan SSML
        is_ssml = processed_text.startswith('<speak>') and processed_text.endswith('</speak>')
        
        # Data untuk request
        data = {
            "text": processed_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.3,  # Lebih rendah untuk variasi yang lebih natural
                "similarity_boost": 0.8,  # Lebih tinggi untuk tetap mirip dengan suara asli
                "style": 0.5,  # Tambahkan sedikit gaya untuk suara lebih ekspresif
                "use_speaker_boost": True
            }
        }
        
        # Tambahkan flag SSML jika teks menggunakan format SSML
        if is_ssml:
            data["text_type"] = "ssml"
        
        # Kirim request ke ElevenLabs API
        print("INFO: Mengirim request ke ElevenLabs API...")
        response = requests.post(url, json=data, headers=headers)
        
        # Periksa status response
        if response.status_code == 200:
            # Simpan audio ke file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"INFO: File audio berhasil disimpan ke {output_path}")
            return True
        else:
            print(f"ERROR: ElevenLabs API mengembalikan status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: Gagal menggunakan ElevenLabs API: {str(e)}")
        return False

# Daftar voice_id yang tersedia (beberapa contoh)
VOICE_IDS = {
    "indonesia_pria": "pNInz6obpgDQGcFmaJgB",  # Contoh ID untuk suara Indonesia pria
    "indonesia_wanita": "EXAVITQu4vr4xnSDxMaL"  # Contoh ID untuk suara Indonesia wanita
}

# Contoh penggunaan
if __name__ == "__main__":
    text_to_speech_elevenlabs(
        "Halo, ini adalah contoh suara yang dihasilkan oleh ElevenLabs.", 
        "test_output.mp3"
    )
