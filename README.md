# Ai-Berbicara: Voice AI Assistant Lokal

Sistem AI assistant berbasis web yang bisa diajak ngobrol pakai suara. Menggunakan Speech-to-Text, LLM lokal (Ollama), dan Text-to-Speech untuk menciptakan pengalaman percakapan yang natural dengan AI.

## Fitur Utama

- 🎤 **Speech-to-Text**: Transkripsi suara menggunakan Google Speech API atau Whisper
- 🧠 **AI Lokal**: Integrasi dengan Ollama (model llama3) untuk respons cerdas
- 🔊 **Text-to-Speech**: Sintesis suara menggunakan gTTS atau Coqui TTS
- 🌐 **Web Interface**: Antarmuka web sederhana untuk interaksi
- 🔄 **Fleksibel**: Bisa beralih antara berbagai model STT dan TTS

## Struktur Project

```text
Ai-Berbicara/
├── backend/
│   ├── app.py                 # Aplikasi Flask utama
│   ├── llm_model/             # Integrasi dengan Ollama LLM
│   │   └── ollama_client.py   # Client untuk Ollama API
│   ├── voice_samples/         # Sampel suara untuk voice cloning
│   └── requirements.txt       # Dependensi Python
├── frontend/
│   ├── index.html            # Halaman web utama
│   ├── script.js             # JavaScript untuk rekam & kirim audio
│   └── style.css             # Styling CSS
├── CHANGELOG.md              # Riwayat perubahan
└── README.md                 # Dokumentasi
```

## Cara Install & Jalankan

### 1. Prasyarat

- Python 3.10 atau lebih baru
- Node.js dan npm (opsional, untuk pengembangan frontend)
- [Ollama](https://ollama.ai/) terinstall dan berjalan
- ffmpeg (untuk pemrosesan audio)

### 2. Setup Backend

```bash
# Clone repository
git clone https://github.com/duwiarsana/Ai-Berbicara.git
cd Ai-Berbicara

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
# atau: venv\Scripts\activate  # Untuk Windows

# Install dependensi
pip install -r backend/requirements.txt

# Jalankan backend
python backend/app.py
```

### 3. Akses Frontend

Cukup buka file `frontend/index.html` di browser Anda atau gunakan server HTTP sederhana.

### 4. Menggunakan Voice Assistant

1. Buka frontend di browser
2. Klik tombol mikrofon untuk mulai merekam
3. Bicara ke mikrofon Anda
4. Rekaman akan dikirim ke backend untuk diproses
5. Dengarkan respons dari AI

## Konfigurasi

### Mengubah Model LLM

Ubah model di `backend/app.py` pada baris yang menggunakan `ask_llm()` dengan parameter model yang berbeda.

### Mengubah Nada Suara

1. Tambahkan file audio (WAV/MP3) ke folder `backend/voice_samples/`
2. Kirim parameter `voice_type` dengan nama file saat mengirim request dari frontend

## Troubleshooting

- **Port 5050 sudah digunakan**: Matikan proses yang menggunakan port tersebut atau ubah port di `app.py`
- **Transkripsi gagal**: Pastikan mikrofon berfungsi dan audio terekam dengan baik
- **Ollama error**: Pastikan Ollama berjalan dengan perintah `ollama serve`
- **Audio tidak terdengar**: Periksa pengaturan audio browser dan volume sistem

## Pengembangan Selanjutnya

- Integrasi Whisper lokal yang lebih baik untuk transkripsi offline
- Fitur riwayat percakapan
- Antarmuka pengguna yang lebih menarik
- Dukungan untuk lebih banyak bahasa
- Optimasi untuk perangkat dengan sumber daya terbatas

---

Dibuat dengan ❤️ oleh Duwi Arsana. Kontribusi dan pengembangan lebih lanjut sangat terbuka!
