import os
import subprocess
import numpy as np
from scipy.io import wavfile
from scipy import signal

def enhance_audio_quality(audio_path):
    """
    Meningkatkan kualitas audio dengan normalisasi, filter, dan penyesuaian lainnya.
    
    Args:
        audio_path (str): Path ke file audio yang akan ditingkatkan
        
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        # Baca file audio
        sample_rate, audio_data = wavfile.read(audio_path)
        
        # Konversi ke float untuk pemrosesan
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
            if audio_data.max() > 1.0:
                audio_data = audio_data / 32767.0  # Normalisasi untuk 16-bit audio
        
        # 1. Normalisasi volume
        max_amplitude = np.max(np.abs(audio_data))
        if max_amplitude > 0:
            normalized_audio = audio_data / max_amplitude * 0.9  # 90% dari maksimum untuk menghindari clipping
        else:
            normalized_audio = audio_data
        
        # 2. Tambahkan sedikit reverb untuk suara lebih natural
        reverb_audio = add_reverb(normalized_audio, sample_rate, room_scale=0.1, wet_level=0.1)
        
        # 3. Perbaiki frekuensi untuk suara lebih jelas
        enhanced_audio = enhance_frequencies(reverb_audio, sample_rate)
        
        # 4. Simpan hasil
        wavfile.write(audio_path, sample_rate, (enhanced_audio * 32767.0).astype(np.int16))
        
        print(f"INFO: Audio berhasil ditingkatkan: {audio_path}")
        return True
        
    except Exception as e:
        print(f"ERROR: Gagal meningkatkan kualitas audio: {str(e)}")
        # Jika gagal, tidak perlu panik, gunakan file asli
        return False

def add_reverb(audio, sample_rate, room_scale=0.2, wet_level=0.2):
    """
    Menambahkan efek reverb ringan untuk suara lebih natural.
    
    Args:
        audio (np.array): Data audio
        sample_rate (int): Sample rate audio
        room_scale (float): Ukuran ruangan (0.0 - 1.0)
        wet_level (float): Level efek (0.0 - 1.0)
        
    Returns:
        np.array: Audio dengan reverb
    """
    # Hitung delay berdasarkan room_scale
    delay_samples = int(sample_rate * room_scale * 0.1)  # 0.1 detik maksimum
    
    # Buat impulse response sederhana
    impulse = np.zeros(delay_samples)
    impulse[0] = 1.0  # Direct sound
    
    # Tambahkan beberapa refleksi
    for i in range(1, 5):
        pos = int(delay_samples * i / 5)
        if pos < delay_samples:
            impulse[pos] = 0.5 / i  # Refleksi dengan atenuasi
    
    # Tambahkan decay
    decay = np.exp(-np.arange(delay_samples) / (sample_rate * room_scale))
    impulse = impulse * decay
    
    # Konvolusi untuk menambahkan reverb
    reverb_audio = signal.convolve(audio, impulse, mode='full')[:len(audio)]
    
    # Mix dry dan wet signals
    result = (1.0 - wet_level) * audio + wet_level * reverb_audio
    
    return result

def enhance_frequencies(audio, sample_rate):
    """
    Meningkatkan frekuensi tertentu untuk suara lebih jelas.
    
    Args:
        audio (np.array): Data audio
        sample_rate (int): Sample rate audio
        
    Returns:
        np.array: Audio dengan frekuensi yang ditingkatkan
    """
    # Desain filter untuk meningkatkan frekuensi suara (1kHz - 3kHz)
    b, a = signal.butter(2, [1000/(sample_rate/2), 3000/(sample_rate/2)], btype='bandpass')
    
    # Terapkan filter
    enhanced = signal.lfilter(b, a, audio)
    
    # Mix dengan audio asli (70% asli, 30% enhanced)
    result = 0.7 * audio + 0.3 * enhanced
    
    # Tambahkan sedikit bass untuk kehangatan suara (100-300Hz)
    b_bass, a_bass = signal.butter(2, 300/(sample_rate/2), btype='lowpass')
    bass_enhanced = signal.lfilter(b_bass, a_bass, audio)
    
    # Mix dengan hasil sebelumnya (90% hasil sebelumnya, 10% bass)
    final_result = 0.9 * result + 0.1 * bass_enhanced
    
    return final_result
