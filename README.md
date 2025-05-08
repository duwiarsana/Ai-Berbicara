# Voice AI Agent Lokal

Sistem AI agent berbasis web, berjalan lokal, bisa diajak ngobrol pakai suara (STT, LLM, TTS lokal).

## Struktur Project

```
voice-ai-agent/
├── backend/
│   ├── app.py
│   ├── whisper_model/
│   ├── tts_model/
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── README.md
```

## Cara Install & Jalankan

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Install whisper, coqui-tts, ollama/llama-cpp-python, dsb sesuai kebutuhan
python app.py
```

### 2. Frontend

Cukup buka `frontend/index.html` di browser (atau pakai simple HTTP server).

### 3. Akses

Buka [http://localhost:5000](http://localhost:5000) untuk backend, dan buka file `index.html` untuk frontend.

### 4. Pengembangan Selanjutnya
- Integrasi Whisper lokal di `backend/whisper_model/`
- Integrasi LLM lokal (Ollama, Llama, Mistral, dsb)
- Integrasi TTS lokal di `backend/tts_model/`
- Perbaiki pengiriman audio dan format jika perlu
- Bisa dikembangkan untuk multi-user, history, dsb

## Catatan
- Semua proses berjalan lokal, tanpa internet.
- Pastikan dependensi sudah terinstall dan model sudah diunduh.
- Untuk demo awal, backend hanya mengembalikan audio yang sama dengan input.

---

Kontribusi dan pengembangan lebih lanjut sangat terbuka!
