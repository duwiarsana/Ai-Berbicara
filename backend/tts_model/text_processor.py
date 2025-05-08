import re

def preprocess_text_for_tts(text):
    """
    Memproses teks untuk meningkatkan kualitas text-to-speech.
    
    Args:
        text (str): Teks input
        
    Returns:
        str: Teks yang telah diproses
    """
    # Tambahkan spasi setelah tanda baca untuk memberikan jeda natural
    text = re.sub(r'([.,!?;:])', r'\1 ', text)
    
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tambahkan markup khusus Bahasa Indonesia
    text = add_indonesian_specific_markup(text)
    
    # Tambahkan SSML untuk tanda baca yang lebih baik (untuk ElevenLabs)
    # Konversi teks ke format SSML
    ssml_text = add_ssml_markup(text)
    
    return ssml_text

def add_ssml_markup(text):
    """
    Menambahkan markup SSML untuk meningkatkan intonasi.
    
    Args:
        text (str): Teks input
        
    Returns:
        str: Teks dengan markup SSML
    """
    # Tambahkan jeda setelah tanda baca
    text = re.sub(r'([.,])', r'\1<break time="200ms"/>', text)
    text = re.sub(r'([!?])', r'\1<break time="400ms"/>', text)
    
    # Tambahkan penekanan pada kata-kata penting
    # Deteksi kata-kata yang mungkin penting (huruf kapital di tengah kalimat)
    words = text.split()
    for i, word in enumerate(words):
        if i > 0 and word[0].isupper() and len(word) > 1:
            words[i] = f'<emphasis level="moderate">{word}</emphasis>'
    
    text = ' '.join(words)
    
    # Atur kecepatan bicara untuk lebih natural (sedikit lebih lambat)
    text = f'<prosody rate="95%">{text}</prosody>'
    
    # Tambahkan variasi pitch untuk intonasi yang lebih natural
    text = f'<prosody pitch="+0%" range="50%">{text}</prosody>'
    
    # Bungkus dalam tag speak
    ssml_text = f'<speak>{text}</speak>'
    
    return ssml_text

def add_indonesian_specific_markup(text):
    """
    Menambahkan markup SSML khusus untuk Bahasa Indonesia.
    
    Args:
        text (str): Teks input
        
    Returns:
        str: Teks dengan markup SSML untuk Bahasa Indonesia
    """
    # Deteksi pola kalimat tanya
    if re.search(r'\?\s*$', text):
        # Untuk kalimat tanya, gunakan intonasi naik di akhir
        text = re.sub(r'([^?]+)(\?\s*)$', r'<prosody pitch="+15%">\1</prosody>\2', text)
    
    # Deteksi pola kalimat seru/perintah
    if re.search(r'!\s*$', text):
        # Untuk kalimat seru, gunakan penekanan dan volume lebih tinggi
        text = re.sub(r'([^!]+)(!\s*)$', r'<prosody volume="+10%" pitch="+5%">\1</prosody>\2', text)
    
    # Tambahkan jeda natural di antara frasa
    text = re.sub(r'(,\s+dan\s+)', r'<break time="150ms"/>\1', text)
    text = re.sub(r'(:\s+)', r'<break time="300ms"/>\1', text)
    
    return text

def preprocess_text_for_coqui(text):
    """
    Memproses teks khusus untuk Coqui TTS.
    
    Args:
        text (str): Teks input
        
    Returns:
        str: Teks yang telah diproses untuk Coqui
    """
    # Tambahkan spasi setelah tanda baca untuk memberikan jeda natural
    text = re.sub(r'([.,!?;:])', r'\1 ', text)
    
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tambahkan tanda khusus untuk jeda
    text = re.sub(r'([.,])', r'\1...', text)  # Jeda pendek
    text = re.sub(r'([!?])', r'\1......', text)  # Jeda panjang
    
    return text
