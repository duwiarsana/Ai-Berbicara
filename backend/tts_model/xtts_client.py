from TTS.api import TTS
import os

def text_to_speech_xtts(text, output_path, speaker_wav):
    """
    Generate speech using Coqui XTTS from a custom speaker wav file.
    Args:
        text (str): Text to synthesize
        output_path (str): Path to save the output wav
        speaker_wav (str): Path to speaker reference wav
    Returns:
        bool: True if success, False if error
    """
    try:
        # You may cache the TTS object for efficiency if needed
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print(f"INFO: Using XTTS to clone from {speaker_wav}")
        wav = tts.tts(text, speaker_wav=speaker_wav, language="id")
        tts.save_wav(wav, output_path)
        print(f"INFO: XTTS audio saved to {output_path}")
        return True
    except Exception as e:
        print(f"ERROR: XTTS failed: {str(e)}")
        return False
