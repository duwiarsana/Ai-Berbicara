import os
from google.cloud import texttospeech

def text_to_speech_google_cloud(text, output_path, language_code="id-ID", voice_name="id-ID-Wavenet-D"):
    """
    Generate speech using Google Cloud TTS (male voice).
    Args:
        text (str): Text to synthesize
        output_path (str): Path to save the output mp3
        language_code (str): Language code (default: Indonesian)
        voice_name (str): Voice name (default: male, Indonesian)
    Returns:
        bool: True if success, False if error
    """
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        print(f"INFO: Google Cloud TTS audio saved to {output_path}")
        return True
    except Exception as e:
        print(f"ERROR: Google Cloud TTS failed: {str(e)}")
        return False
