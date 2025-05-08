# Changelog

Semua perubahan penting pada proyek ini akan didokumentasikan di file ini.

## [0.2.0] - 2025-05-08

### Ditambahkan

- Integrasi SpeechRecognition dengan Google Speech API sebagai alternatif Whisper
- Implementasi fallback mechanism untuk transkripsi audio
- Dukungan untuk pemilihan nada suara (voice cloning) di Coqui TTS
- Folder `voice_samples` untuk menyimpan sampel suara referensi
- Endpoint GET `/api/voice` yang mengembalikan daftar suara yang tersedia
- Log detail untuk memudahkan debugging
- Penanganan error yang lebih baik di seluruh aplikasi

### Diperbaiki

- Masalah transkripsi audio dengan Whisper
- Masalah port 5050 yang sudah digunakan
- Masalah pengiriman file audio dari backend ke frontend
- Masalah audio tidak terdengar di browser
- Penanganan CORS untuk memastikan komunikasi frontend-backend lancar

### Teknis

- Konversi audio menggunakan ffmpeg untuk format yang kompatibel
- Implementasi voice cloning dengan XTTS v2
- Penggunaan parameter `voice_type` untuk memilih suara
- Perbaikan header CORS dan pengaturan `as_attachment=false`
- Pencegahan penghapusan file audio prematur

### Diketahui

- Coqui TTS memerlukan download model besar (~1GB) saat pertama kali digunakan
- Transkripsi dengan Google Speech API memerlukan koneksi internet
- Ollama harus dijalankan terpisah dengan perintah `ollama serve`

## [0.1.0] - 2025-05-08

### Ditambahkan
- Sistem dasar Voice AI Agent lokal
- Integrasi Whisper untuk Speech-to-Text
- Integrasi Ollama (Llama3) untuk LLM
- Integrasi gTTS untuk Text-to-Speech
- Frontend sederhana untuk merekam dan memutar audio
- Backend Flask dengan API untuk memproses audio
- Dokumentasi dasar di README.md

### Teknis
- Whisper untuk transkripsi audio
- Ollama dengan model Llama3 untuk respons AI
- gTTS untuk sintesis suara
- Flask sebagai backend API
- Sistem berjalan lokal dengan beberapa komponen online

### Diketahui
- Masalah dengan transkripsi Whisper
- Perlu waktu untuk mendownload model saat pertama kali dijalankan
- Belum ada fitur riwayat percakapan
