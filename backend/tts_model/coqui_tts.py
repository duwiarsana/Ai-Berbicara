import os
import tempfile
import uuid
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

class CoquiTTS:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_name=None):
        """
        Initialize Coqui TTS dengan model tertentu.
        
        Args:
            model_name (str): Nama model TTS yang akan digunakan
            vocoder_name (str, optional): Nama vocoder (jika None, akan menggunakan default)
        """
        self.model_name = model_name
        self.vocoder_name = vocoder_name
        
        # Inisialisasi model manager dan synthesizer
        self.manager = ModelManager()
        self.model_path, self.config_path, self.model_item = self.manager.download_model(model_name)
        
        if vocoder_name is not None:
            self.vocoder_path, self.vocoder_config_path, _ = self.manager.download_model(vocoder_name)
            self.synthesizer = Synthesizer(
                self.model_path, self.config_path, self.vocoder_path, self.vocoder_config_path
            )
        else:
            self.synthesizer = Synthesizer(self.model_path, self.config_path)
    
    def text_to_speech(self, text, output_path=None):
        """
        Mengubah teks menjadi suara dan menyimpannya ke file.
        
        Args:
            text (str): Teks yang akan diubah menjadi suara
            output_path (str, optional): Path untuk menyimpan file audio
                                         Jika None, akan membuat file temporary
        
        Returns:
            str: Path ke file audio hasil
        """
        if output_path is None:
            # Buat file temporary dengan ekstensi .wav
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"tts_output_{uuid.uuid4()}.wav")
        
        # Synthesize teks menjadi audio
        wavs = self.synthesizer.tts(text)
        
        # Simpan audio ke file
        self.synthesizer.save_wav(wavs, output_path)
        
        return output_path

def text_to_speech(text, output_path=None, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    """
    Fungsi helper untuk mengubah teks menjadi suara.
    
    Args:
        text (str): Teks yang akan diubah menjadi suara
        output_path (str, optional): Path untuk menyimpan file audio
        model_name (str): Nama model TTS yang akan digunakan
    
    Returns:
        str: Path ke file audio hasil
    """
    tts = CoquiTTS(model_name=model_name)
    return tts.text_to_speech(text, output_path)

# Contoh penggunaan
if __name__ == "__main__":
    output_file = text_to_speech(
        "Halo, ini adalah contoh text to speech menggunakan Coqui TTS.",
        model_name="tts_models/en/ljspeech/tacotron2-DDC"
    )
    print(f"Audio disimpan di: {output_file}")
