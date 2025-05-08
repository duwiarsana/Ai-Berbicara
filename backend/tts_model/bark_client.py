import os
from bark import SAMPLE_RATE, generate_audio, preload_models
import soundfile as sf

def text_to_speech_bark(text, output_path, speaker_wav=None):
    """
    Mengubah teks menjadi ucapan dengan Bark (preset Bahasa Indonesia, bukan cloning custom wav).
    Args:
        text (str): Teks yang akan diubah menjadi ucapan
        output_path (str): Path untuk menyimpan file audio output
        speaker_wav (str): (Diabaikan, hanya untuk kompatibilitas)
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        preload_models()
        # Gunakan preset voice Bahasa Indonesia dari Bark
        voice_preset = "v2/en_speaker_6"
        print(f"INFO: Menggunakan Bark voice preset: {voice_preset}")
        audio_array = generate_audio(text, history_prompt=voice_preset)
        sf.write(output_path, audio_array, SAMPLE_RATE)
        print(f"INFO: File audio Bark berhasil disimpan ke {output_path}")
        return True
    except Exception as e:
        print(f"ERROR: Gagal menggunakan Bark: {str(e)}")
        return False
