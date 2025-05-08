# Changelog

Semua perubahan penting pada proyek ini akan didokumentasikan di file ini.

## [0.1.0] - 2025-05-08

### Ditambahkan
- Sistem dasar Voice AI Agent lokal
- Integrasi Whisper untuk Speech-to-Text
- Integrasi Ollama (Llama3) untuk LLM
- Integrasi Coqui TTS untuk Text-to-Speech
- Frontend sederhana dengan Tailwind CSS
- Backend Flask dengan API untuk memproses audio
- Dokumentasi dasar di README.md

### Teknis
- Whisper lokal untuk transkripsi audio
- Ollama dengan model Llama3 untuk respons AI
- Coqui TTS dengan model Tacotron2 untuk sintesis suara
- Flask sebagai backend API
- Tailwind CSS untuk styling frontend
- Sistem berjalan sepenuhnya lokal tanpa internet

### Diketahui
- Model TTS menggunakan model bahasa Inggris, pengucapan Bahasa Indonesia mungkin tidak sempurna
- Perlu waktu untuk mendownload model saat pertama kali dijalankan
- Belum ada fitur riwayat percakapan
